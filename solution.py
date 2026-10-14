name: Autonomous PR Reviewer Agent

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  ai-code-review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
      issues: write

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0 # Need full history to compute git diff

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install Dependencies
        run: |
          pip install google-genai

      - name: Run Reviewer Agent on Git Diff
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          PR_TITLE: ${{ github.event.pull_request.title }}
          PR_BODY: ${{ github.event.pull_request.body || '' }}
          BASE_REF: ${{ github.event.pull_request.base.ref }}
        run: |
          python - << 'EOF'
          import os
          import subprocess
          import time
          from google import genai

          client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
          base_ref = os.environ.get("BASE_REF", "main")
          pr_title = os.environ.get("PR_TITLE", "")
          pr_body = os.environ.get("PR_BODY", "")

          # STEP 1: Compute the PR's exact Git Diff
          diff_cmd = subprocess.run(["git", "diff", f"origin/{base_ref}...HEAD"], capture_output=True, text=True)
          git_diff = diff_cmd.stdout.strip()

          if not git_diff:
              print("No changes detected in diff.")
              with open("review.md", "w") as f:
                  f.write("### 🤖 Autonomous PR Review\nNo code changes detected in this PR.")
              exit(0)

          # STEP 2: Read AGENTS.md if present
          repo_rules = ""
          if os.path.exists("AGENTS.md"):
              repo_rules = open("AGENTS.md").read()

          # STEP 3: Senior Reviewer Persona Prompt
          review_prompt = f"""
          You are a Staff Software Engineer conducting a thorough, constructive code review on a GitHub Pull Request.

          PR Title: {pr_title}
          PR Description: {pr_body}

          === REPOSITORY ARCHITECTURE GUIDELINES (AGENTS.md) ===
          {repo_rules}
          =======================================================

          === PULL REQUEST CODE DIFF ===
          {git_diff}
          ==============================

          Please produce a structured code review in GitHub Markdown with the following sections:
          1. 📋 Summary of Changes: A brief 2-sentence overview of what this PR does.
          2. 🛡️ Architectural & AGENTS.md Compliance: Check if the code follows repository rules (headers, custom exceptions, docstrings, typing).
          3. ⚠️ Potential Bugs & Edge Cases: Identify any logical flaws, unhandled edge cases (e.g., division by zero, null/empty inputs, concurrency issues).
          4. 💡 Actionable Improvement Suggestions: Provide concrete code suggestions using GitHub suggestion blocks (` ```suggestion ... ``` `).
          5. 🏁 Final Verdict: Select one of:
             - ✅ APPROVED (Ready to merge)
             - 🟡 APPROVED WITH MINOR SUGGESTIONS
             - 🔴 CHANGES REQUESTED (Critical issues must be addressed)
          """

          models = ["models/gemini-3.7-flash", "models/gemini-3.8-flash", "models/gemini-flash-latest"]
          review_content = None

          for m in models:
              try:
                  print(f"🤖 Reviewer analyzing diff using {m}...")
                  res = client.models.generate_content(
                      model=m,
                      contents=review_prompt
                  )
                  review_content = res.text
                  print("✅ Review generated successfully!")
                  break
              except Exception as e:
                  print(f"⚠️ {m} busy: {e}. Retrying in 3s...")
                  time.sleep(3)

          if not review_content:
              review_content = "### 🤖 Autonomous PR Review\nCould not complete AI review due to transient service capacity."

          with open("review.md", "w", encoding="utf-8") as f:
              f.write(review_content)
          EOF

      - name: Post Review Comment to PR
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          gh pr comment ${{ github.event.pull_request.number }} --body-file review.md
