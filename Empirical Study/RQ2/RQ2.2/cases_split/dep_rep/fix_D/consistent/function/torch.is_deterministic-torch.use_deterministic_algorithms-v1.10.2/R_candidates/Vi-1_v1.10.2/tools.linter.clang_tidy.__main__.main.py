def main() -> None:
    options = parse_args()

    if not pathlib.Path("build").exists():
        generate_build_files()

    # Check if clang-tidy executable exists
    exists = os.access(options.clang_tidy_exe, os.X_OK)

    if not exists:
        msg = (
            f"Could not find '{options.clang_tidy_exe}'\n"
            + "We provide a custom build of clang-tidy that has additional checks.\n"
            + "You can install it by running:\n"
            + "$ python3 -m tools.linter.install.clang_tidy \n"
            + "from the pytorch folder"
        )
        raise RuntimeError(msg)

    result, _ = run(options)
    sys.exit(result.returncode)
