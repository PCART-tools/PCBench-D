    def get_command_ex(
        self, file: str, title: str | None = None, **options: Any
    ) -> tuple[str, str]:
        command = executable = "display"
        if title:
            command += f" -title {quote(title)}"
        return command, executable
