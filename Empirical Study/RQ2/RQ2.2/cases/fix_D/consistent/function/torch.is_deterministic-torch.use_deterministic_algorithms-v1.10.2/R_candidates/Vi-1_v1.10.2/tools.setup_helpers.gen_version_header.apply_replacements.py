def apply_replacements(replacements: Dict[str, str], text: str) -> str:
    """
    Applies the given replacements within the text.

    Args:
      replacements (dict): Mapping of str -> str replacements.
      text (str): Text in which to make replacements.

    Returns:
      Text with replacements applied, if any.
    """
    for (before, after) in replacements.items():
        text = text.replace(before, after)
    return text
