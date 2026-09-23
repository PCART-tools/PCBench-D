    def show_file(self, path: str, **options: Any) -> int:
        """
        Display given file.
        """
        subprocess.Popen(["xdg-open", path])
        return 1
