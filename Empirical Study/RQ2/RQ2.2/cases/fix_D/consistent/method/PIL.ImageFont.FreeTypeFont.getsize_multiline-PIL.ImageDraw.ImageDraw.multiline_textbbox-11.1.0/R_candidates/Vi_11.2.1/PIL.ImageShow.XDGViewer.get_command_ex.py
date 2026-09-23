    def get_command_ex(self, file: str, **options: Any) -> tuple[str, str]:
        command = executable = "xdg-open"
        return command, executable
