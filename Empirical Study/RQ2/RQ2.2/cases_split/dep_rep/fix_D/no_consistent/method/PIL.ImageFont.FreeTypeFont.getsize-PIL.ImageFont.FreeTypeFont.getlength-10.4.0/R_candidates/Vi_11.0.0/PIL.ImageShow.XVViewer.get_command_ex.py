    def get_command_ex(
        self, file: str, title: str | None = None, **options: Any
    ) -> tuple[str, str]:
        # note: xv is pretty outdated.  most modern systems have
        # imagemagick's display command instead.
        command = executable = "xv"
        if title:
            command += f" -name {quote(title)}"
        return command, executable
