    def show_file(self, path, **options):
        """
        Display given file.
        """
        os.system(self.get_command(path, **options))  # nosec
        return 1
