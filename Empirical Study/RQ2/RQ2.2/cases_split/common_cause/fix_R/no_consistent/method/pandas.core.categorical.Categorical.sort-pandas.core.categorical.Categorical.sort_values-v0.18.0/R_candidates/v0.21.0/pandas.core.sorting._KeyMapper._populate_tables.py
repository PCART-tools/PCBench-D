    def _populate_tables(self):
        for labs, table in zip(self.labels, self.tables):
            table.map(self.comp_ids, labs.astype(np.int64))
