def apply_nolint(fname: str, warnings: Dict[int, Set[str]]) -> None:
    with open(fname, encoding="utf-8") as f:
        lines = f.readlines()

    line_offset = -1  # As in .cpp files lines are numbered starting from 1
    for line_no in sorted(warnings.keys()):
        nolint_diagnostics = ",".join(warnings[line_no])
        line_no += line_offset
        indent = " " * (len(lines[line_no]) - len(lines[line_no].lstrip(" ")))
        lines.insert(line_no, f"{indent}// NOLINTNEXTLINE({nolint_diagnostics})\n")
        line_offset += 1

    with open(fname, mode="w") as f:
        f.write("".join(lines))
