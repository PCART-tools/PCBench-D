    def show_file(self, path, **options):
        """
        Display given file.
        """
        subprocess.Popen(["xdg-open", path])
        return 1
