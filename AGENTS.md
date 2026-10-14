# Enterprise Repository Architecture Guidelines

All AI Coding Agents MUST strictly adhere to these rules before writing code:

## 1. Header Requirement
Every `solution.py` file MUST begin with this exact header comment on line 1:
`# ARCHITECTURE COMPLIANT: AGENTS.MD v1.0`

## 2. Error Handling Standard
- NEVER raise bare `Exception` or generic `ValueError` directly.
- Always define and raise a custom domain exception class inheriting from `Exception` (e.g. `ValidationError` or `DomainServiceError`).

## 3. Documentation Standard
- Every function must include a full Google-style docstring detailing:
  - Description
  - `Args:`
  - `Returns:`
  - `Raises:`

## 4. Strict Type Hints
- All parameters and return values must be fully type-hinted using Python's `typing` module.
