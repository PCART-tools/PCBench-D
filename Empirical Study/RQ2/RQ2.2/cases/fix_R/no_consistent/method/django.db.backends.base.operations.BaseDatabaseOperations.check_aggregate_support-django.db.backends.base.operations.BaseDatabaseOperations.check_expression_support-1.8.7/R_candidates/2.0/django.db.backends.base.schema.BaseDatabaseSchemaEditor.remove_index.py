    def remove_index(self, model, index):
        """Remove an index from a model."""
        self.execute(index.remove_sql(model, self))
