def repair_depfile(depfile: TextIO, include_dirs: List[Path]) -> None:
    changes_made = False
    out = ""
    for line in depfile.readlines():
        if ":" in line:
            colon_pos = line.rfind(":")
            out += line[: colon_pos + 1]
            line = line[colon_pos + 1 :]

        line = line.strip()

        if line.endswith("\\"):
            end = " \\"
            line = line[:-1].strip()
        else:
            end = ""

        path = Path(line)
        if not path.is_absolute():
            changes_made = True
            path = resolve_include(path, include_dirs)
        out += f"    {path}{end}\n"

    # If any paths were changed, rewrite the entire file
    if changes_made:
        depfile.seek(0)
        depfile.write(out)
        depfile.truncate()
