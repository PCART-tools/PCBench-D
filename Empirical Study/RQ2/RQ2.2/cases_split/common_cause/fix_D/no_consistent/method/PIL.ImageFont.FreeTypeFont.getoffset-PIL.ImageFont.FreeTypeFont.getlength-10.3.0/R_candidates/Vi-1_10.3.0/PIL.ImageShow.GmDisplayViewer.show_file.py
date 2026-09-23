    def show_file(self, path: str, **options: Any) -> int:
        """
        Display given file.
        """
        subprocess.Popen(["gm", "display", path])
        return 1
