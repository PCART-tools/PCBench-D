    def get_command_ex(self, file: str, **options: Any) -> tuple[str, str]:
        executable = "eog"
        command = "eog -n"
        return command, executable
