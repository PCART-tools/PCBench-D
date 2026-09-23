def extract_include_arg(include_dirs: List[Path], i: int, args: List[str]) -> None:
    def extract_one(name: str, i: int, args: List[str]) -> Optional[str]:
        arg = args[i]
        if arg == name:
            return args[i + 1]
        if arg.startswith(name):
            arg = arg[len(name) :]
            return arg[1:] if arg[0] == "=" else arg
        return None

    for name in PRE_INCLUDE_ARGS:
        path = extract_one(name, i, args)
        if path is not None:
            include_dirs.insert(0, Path(path).resolve())
            return

    for name in POST_INCLUDE_ARGS:
        path = extract_one(name, i, args)
        if path is not None:
            include_dirs.append(Path(path).resolve())
            return
