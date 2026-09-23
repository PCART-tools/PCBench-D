        def next(self):
            row = next(self.reader)
            return [compat.text_type(s, "utf-8") for s in row]
