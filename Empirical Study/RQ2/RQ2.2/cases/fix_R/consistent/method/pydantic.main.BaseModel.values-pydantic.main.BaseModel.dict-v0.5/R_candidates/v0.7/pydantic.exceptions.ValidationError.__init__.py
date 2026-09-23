    def __init__(self, errors):
        self.errors_raw = errors
        e_count = len(errors)
        self.message = 'error validating input' if e_count == 1 else f'{e_count} errors validating input'
        super().__init__(self.message)
