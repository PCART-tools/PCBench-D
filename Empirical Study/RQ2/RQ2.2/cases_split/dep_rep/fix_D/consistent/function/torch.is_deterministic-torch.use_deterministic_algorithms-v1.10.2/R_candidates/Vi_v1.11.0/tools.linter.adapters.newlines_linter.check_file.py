def check_file(filename: str) -> Optional[LintMessage]:
    logging.debug("Checking file %s", filename)

    with open(filename, "rb") as f:
        a = len(f.read(2))
        if a == 0:
            # File is empty, just leave it alone.
            return None
        elif a == 1:
            # file is wrong whether or not the only byte is a newline
            return LintMessage(
                path=filename,
                line=None,
                char=None,
                code=LINTER_CODE,
                severity=LintSeverity.ERROR,
                name="testestTrailing newline",
                original=None,
                replacement=None,
                description="Trailing newline found. Run `lintunner --take NEWLINE -a` to apply changes.",
            )

        else:
            # Read the last two bytes
            f.seek(-2, os.SEEK_END)
            b, c = f.read(2)
            # no ASCII byte is part of any non-ASCII character in UTF-8
            if b != NEWLINE and c == NEWLINE:
                return None
            else:
                f.seek(0)
                try:
                    original = f.read().decode("utf-8")
                except Exception as err:
                    return LintMessage(
                        path=filename,
                        line=None,
                        char=None,
                        code=LINTER_CODE,
                        severity=LintSeverity.ERROR,
                        name="Decoding failure",
                        original=None,
                        replacement=None,
                        description=f"utf-8 decoding failed due to {err.__class__.__name__}:\n{err}",
                    )

                return LintMessage(
                    path=filename,
                    line=None,
                    char=None,
                    code=LINTER_CODE,
                    severity=LintSeverity.ERROR,
                    name="Trailing newline",
                    original=original,
                    replacement=original.rstrip("\n") + "\n",
                    description="Trailing newline found. Run `lintunner --take NEWLINE -a` to apply changes.",
                )
