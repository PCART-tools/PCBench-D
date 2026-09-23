    def process_clob(self, value):
        if value is None:
            return ''
        return force_text(value.read())
