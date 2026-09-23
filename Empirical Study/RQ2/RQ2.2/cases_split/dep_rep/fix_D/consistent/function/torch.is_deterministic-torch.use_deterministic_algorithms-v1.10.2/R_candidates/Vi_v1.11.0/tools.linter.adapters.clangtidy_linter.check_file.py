def check_file(
    filename: str,
    binary: str,
    build_dir: Path,
) -> List[LintMessage]:
    try:
        proc = run_command(
            [binary, f"-p={build_dir}", *include_args, filename],
        )
    except (OSError) as err:
        return [
            LintMessage(
                path=filename,
                line=None,
                char=None,
                code="CLANGTIDY",
                severity=LintSeverity.ERROR,
                name="command-failed",
                original=None,
                replacement=None,
                description=(
                    f"Failed due to {err.__class__.__name__}:\n{err}"
                ),
            )
        ]
    lint_messages = []
    try:
        # Change the current working directory to the build directory, since
        # clang-tidy will report files relative to the build directory.
        saved_cwd = os.getcwd()
        os.chdir(build_dir)

        for match in RESULTS_RE.finditer(proc.stdout.decode()):
            # Convert the reported path to an absolute path.
            abs_path = str(Path(match["file"]).resolve())
            message = LintMessage(
                path=abs_path,
                name=match["code"],
                description=match["message"],
                line=int(match["line"]),
                char=int(match["column"])
                if match["column"] is not None and not match["column"].startswith("-")
                else None,
                code="CLANGTIDY",
                severity=severities.get(match["severity"], LintSeverity.ERROR),
                original=None,
                replacement=None,
            )
            lint_messages.append(message)
    finally:
        os.chdir(saved_cwd)

    return lint_messages
