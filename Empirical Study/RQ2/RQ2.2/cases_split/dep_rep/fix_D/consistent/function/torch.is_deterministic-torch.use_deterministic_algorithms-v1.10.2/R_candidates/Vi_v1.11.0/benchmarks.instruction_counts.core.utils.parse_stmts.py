def parse_stmts(stmts: str) -> Tuple[str, str]:
    """Helper function for side-by-side Python and C++ stmts.

    For more complex statements, it can be useful to see Python and C++ code
    side by side. To this end, we provide an **extremely restricted** way
    to define Python and C++ code side-by-side. The schema should be mostly
    self explanatory, with the following non-obvious caveats:
      - Width for the left (Python) column MUST be 40 characters.
      - The column separator is " | ", not "|". Whitespace matters.
    """
    stmts = textwrap.dedent(stmts).strip()
    lines: List[str] = stmts.splitlines(keepends=False)
    assert len(lines) >= 3, f"Invalid string:\n{stmts}"

    column_header_pattern = r"^Python\s{35}\| C\+\+(\s*)$"
    signature_pattern = r"^: f\((.*)\)( -> (.+))?\s*$"
    separation_pattern = r"^[-]{40} | [-]{40}$"
    code_pattern = r"^(.{40}) \|($| (.*)$)"

    column_match = re.search(column_header_pattern, lines[0])
    if column_match is None:
        raise ValueError(
            f"Column header `{lines[0]}` "
            f"does not match pattern `{column_header_pattern}`")

    assert re.search(separation_pattern, lines[1])

    py_lines: List[str] = []
    cpp_lines: List[str] = []
    for l in lines[2:]:
        l_match = re.search(code_pattern, l)
        if l_match is None:
            raise ValueError(f"Invalid line `{l}`")
        py_lines.append(l_match.groups()[0])
        cpp_lines.append(l_match.groups()[2] or "")

        # Make sure we can round trip for correctness.
        l_from_stmts = f"{py_lines[-1]:<40} | {cpp_lines[-1]:<40}".rstrip()
        assert l_from_stmts == l.rstrip(), f"Failed to round trip `{l}`"

    return "\n".join(py_lines), "\n".join(cpp_lines)
