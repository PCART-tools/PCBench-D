    def show_file(self, path: str, **options: Any) -> int:
        """
        Display given file.
        """
        subprocess.Popen(["eog", "-n", path])
        return 1
