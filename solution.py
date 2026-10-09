def reverse_string(s: str) -> str:
    """Return the reversed version of the given string."""
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    return s[::-1]


def is_palindrome(s: str, case_sensitive: bool = False, ignore_whitespace: bool = True) -> bool:
    """Check if the given string is a palindrome.

    Args:
        s: The string to check.
        case_sensitive: Whether the comparison should be case-sensitive. Defaults to False.
        ignore_whitespace: Whether whitespace should be ignored. Defaults to True.

    Returns:
        True if the string is a palindrome, False otherwise.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string")

    processed = s
    if ignore_whitespace:
        processed = "".join(processed.split())
    if not case_sensitive:
        processed = processed.lower()

    return processed == processed[::-1]
