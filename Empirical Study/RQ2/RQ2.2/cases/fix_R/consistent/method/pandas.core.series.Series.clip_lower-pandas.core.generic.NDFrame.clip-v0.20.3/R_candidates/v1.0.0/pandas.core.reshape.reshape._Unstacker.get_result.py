    def get_result(self):
        values, _ = self.get_new_values()
        columns = self.get_new_columns()
        index = self.get_new_index()

        return self.constructor(values, index=index, columns=columns)
