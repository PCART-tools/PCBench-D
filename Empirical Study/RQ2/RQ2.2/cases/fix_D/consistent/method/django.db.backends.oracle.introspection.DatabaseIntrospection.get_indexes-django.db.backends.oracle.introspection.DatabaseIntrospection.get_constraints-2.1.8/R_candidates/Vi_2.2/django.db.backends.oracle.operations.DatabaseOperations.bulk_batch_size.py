    def bulk_batch_size(self, fields, objs):
        """Oracle restricts the number of parameters in a query."""
        if fields:
            return self.connection.features.max_query_params // len(fields)
        return len(objs)
