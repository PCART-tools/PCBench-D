    def show_file(self, path, **options):
        """
        Display given file.
        """
        subprocess.Popen(["eog", "-n", path])
        return 1
