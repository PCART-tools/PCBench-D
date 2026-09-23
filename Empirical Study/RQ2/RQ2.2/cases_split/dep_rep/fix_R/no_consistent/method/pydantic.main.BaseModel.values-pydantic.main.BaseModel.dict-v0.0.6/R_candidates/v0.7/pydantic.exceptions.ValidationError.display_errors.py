    @property
    def display_errors(self):
        return '\n'.join('  ' * i + msg for i, msg in _render_errors(self.errors_dict))
