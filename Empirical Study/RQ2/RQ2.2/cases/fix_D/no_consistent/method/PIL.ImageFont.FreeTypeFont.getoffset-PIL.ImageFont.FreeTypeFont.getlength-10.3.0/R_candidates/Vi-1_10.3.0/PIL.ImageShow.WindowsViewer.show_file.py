    def show_file(self, path: str, **options: Any) -> int:
        """
        Display given file.
        """
        subprocess.Popen(
            self.get_command(path, **options),
            shell=True,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW"),
        )  # nosec
        return 1
