    def get_command_ex(self, file, title=None, **options):
        command = executable = "display"
        if title:
            command += f" -title {quote(title)}"
        return command, executable
