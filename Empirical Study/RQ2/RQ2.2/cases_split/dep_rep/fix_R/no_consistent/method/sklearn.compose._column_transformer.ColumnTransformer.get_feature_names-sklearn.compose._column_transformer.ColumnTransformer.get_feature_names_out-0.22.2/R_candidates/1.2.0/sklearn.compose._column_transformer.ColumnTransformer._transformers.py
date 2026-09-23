    @_transformers.setter
    def _transformers(self, value):
        try:
            self.transformers = [
                (name, trans, col)
                for ((name, trans), (_, _, col)) in zip(value, self.transformers)
            ]
        except (TypeError, ValueError):
            self.transformers = value
