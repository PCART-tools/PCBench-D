def lint_file(
    matching_line: str,
    replace_pattern: str,
    linter_name: str,
    error_name: str,
    error_description: str,
) -> LintMessage:
    # matching_line looks like:
    #   tools/linter/clangtidy_linter.py:13:import foo.bar.baz
    split = matching_line.split(":")
    filename = split[0]

    original = None
    replacement = None
    if replace_pattern:
        with open(filename, "r") as f:
            original = f.read()

        try:
            proc = run_command(["sed", "-r", replace_pattern, filename])
            replacement = proc.stdout.decode("utf-8")
        except Exception as err:
            return LintMessage(
                path=None,
                line=None,
                char=None,
                code=linter_name,
                severity=LintSeverity.ERROR,
                name="command-failed",
                original=None,
                replacement=None,
                description=(
                    f"Failed due to {err.__class__.__name__}:\n{err}"
                    if not isinstance(err, subprocess.CalledProcessError)
                    else (
                        "COMMAND (exit code {returncode})\n"
                        "{command}\n\n"
                        "STDERR\n{stderr}\n\n"
                        "STDOUT\n{stdout}"
                    ).format(
                        returncode=err.returncode,
                        command=" ".join(as_posix(x) for x in err.cmd),
                        stderr=err.stderr.decode("utf-8").strip() or "(empty)",
                        stdout=err.stdout.decode("utf-8").strip() or "(empty)",
                    )
                ),
            )

    return LintMessage(
        path=split[0],
        line=int(split[1]),
        char=None,
        code=linter_name,
        severity=LintSeverity.ERROR,
        name=error_name,
        original=original,
        replacement=replacement,
        description=error_description,
    )
