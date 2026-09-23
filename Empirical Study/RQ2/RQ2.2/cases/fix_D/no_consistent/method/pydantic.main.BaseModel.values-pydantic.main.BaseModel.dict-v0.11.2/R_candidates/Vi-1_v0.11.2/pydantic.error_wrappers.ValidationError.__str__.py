    def __str__(self):
        errors = self.errors()
        no_errors = len(errors)
        return f'{no_errors} validation error{"" if no_errors == 1 else "s"}\n{display_errors(errors)}'
