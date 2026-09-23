def normalize_source_lines(sourcelines: List[str]) -> List[str]:
    """
    This helper function accepts a list of source lines. It finds the
    indentation level of the function definition (`def`), then it indents
    all lines in the function body to a point at or greater than that
    level. This allows for comments and continued string literals that
    are at a lower indentation than the rest of the code.
    Args:
        sourcelines: function source code, separated into lines by
                        the '\n' character
    Returns:
        A list of source lines that have been correctly aligned
    """

    def remove_prefix(text, prefix):
        return text[text.startswith(prefix) and len(prefix):]

    # Find the line and line number containing the function definition
    for i, l in enumerate(sourcelines):
        if l.lstrip().startswith("def"):
            idx = i
            break
    fn_def = sourcelines[idx]

    # Get a string representing the amount of leading whitespace
    whitespace = fn_def.split("def")[0]

    # Add this leading whitespace to all lines before and after the `def`
    aligned_prefix = [whitespace + remove_prefix(s, whitespace) for s in sourcelines[:idx]]
    aligned_suffix = [whitespace + remove_prefix(s, whitespace) for s in sourcelines[idx + 1:]]

    # Put it together again
    aligned_prefix.append(fn_def)
    return aligned_prefix + aligned_suffix
