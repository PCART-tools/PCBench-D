    def get_key(self, comp_id):
        return tuple(
            level[table.get_item(comp_id)]
            for table, level in zip(self.tables, self.levels)
        )
