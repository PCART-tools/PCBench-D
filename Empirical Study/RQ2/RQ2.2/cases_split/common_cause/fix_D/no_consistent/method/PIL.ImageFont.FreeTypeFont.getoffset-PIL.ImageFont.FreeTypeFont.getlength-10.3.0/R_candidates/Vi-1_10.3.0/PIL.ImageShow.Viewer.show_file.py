    def show_file(self, path: str, **options: Any) -> int:
        """
        Display given file.
        """
        os.system(self.get_command(path, **options))  # nosec
        return 1
