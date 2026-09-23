    def clear(self):
        # docstring inherited
        super().clear()
        self.yaxis.set_major_formatter(NullFormatter())
