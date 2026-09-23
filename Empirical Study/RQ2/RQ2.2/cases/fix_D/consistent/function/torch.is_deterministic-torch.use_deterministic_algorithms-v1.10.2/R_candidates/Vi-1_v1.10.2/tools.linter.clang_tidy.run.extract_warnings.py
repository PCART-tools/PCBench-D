def extract_warnings(
    output: str, base_dir: str = "."
) -> Tuple[Dict[str, Dict[int, Set[str]]], List[ClangTidyWarning]]:
    warn2occ: Dict[str, List[Tuple[str, int]]] = {}
    fixes: Dict[str, Dict[int, Set[str]]] = {}
    for line in output.splitlines():
        p = CLANG_WARNING_PATTERN.match(line)
        if p is None:
            continue
        if os.path.isabs(p.group(1)):
            path = os.path.abspath(p.group(1))
        else:
            path = os.path.abspath(os.path.join(base_dir, p.group(1)))
        line_no = int(p.group(2))

        # Filter out any options (which start with '-')
        warning_names = set([w for w in p.group(4).split(",") if not w.startswith("-")])

        for name in warning_names:
            if name not in warn2occ:
                warn2occ[name] = []
            warn2occ[name].append((path, line_no))

        if path not in fixes:
            fixes[path] = {}
        if line_no not in fixes[path]:
            fixes[path][line_no] = set()
        fixes[path][line_no].update(warning_names)

    warnings = [ClangTidyWarning(name, sorted(occ)) for name, occ in warn2occ.items()]

    return fixes, warnings
