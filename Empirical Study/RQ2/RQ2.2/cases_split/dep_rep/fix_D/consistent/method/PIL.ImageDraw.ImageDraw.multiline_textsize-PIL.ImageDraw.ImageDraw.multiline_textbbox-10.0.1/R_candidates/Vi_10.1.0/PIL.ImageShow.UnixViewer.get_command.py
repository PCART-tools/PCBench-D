    def get_command(self, file, **options):
        command = self.get_command_ex(file, **options)[0]
        return f"({command} {quote(file)}"
