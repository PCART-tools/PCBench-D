    def add_index(self, model, index):
        """Add an index on a model."""
        self.execute(index.create_sql(model, self))
