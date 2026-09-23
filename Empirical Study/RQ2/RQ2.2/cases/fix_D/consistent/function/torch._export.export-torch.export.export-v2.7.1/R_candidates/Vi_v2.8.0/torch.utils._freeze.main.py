def main() -> None:
    parser = argparse.ArgumentParser(description="Compile py source")
    parser.add_argument("paths", nargs="*", help="Paths to freeze.")
    parser.add_argument("--verbose", action="store_true", help="Print debug logs")
    parser.add_argument(
        "--install-dir", "--install_dir", help="Root directory for all output files"
    )
    parser.add_argument(
        "--oss",
        action="store_true",
        help="If it's OSS build, add a fake _PyImport_FrozenModules",
    )
    parser.add_argument(
        "--symbol-name",
        "--symbol_name",
        help="The name of the frozen module array symbol to generate",
        default="_PyImport_FrozenModules_torch",
    )

    args = parser.parse_args()

    f = Freezer(args.verbose)

    for p in args.paths:
        path = Path(p)
        if path.is_dir() and not Path.exists(path / "__init__.py"):
            # this 'top level path p' is a standard directory containing modules,
            # not a module itself
            # each 'mod' could be a dir containing __init__.py or .py file
            # NB: sorted to make sure this is deterministic
            for mod in sorted(path.glob("*")):
                f.compile_path(mod, mod)
        else:
            f.compile_path(path, path)

    f.write_bytecode(args.install_dir)
    f.write_main(args.install_dir, args.oss, args.symbol_name)
