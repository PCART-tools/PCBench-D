    def show_file(self, path, **options):
        """
        Display given file.
        """
        subprocess.Popen(["gm", "display", path])
        return 1
