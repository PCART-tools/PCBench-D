    def _slice(self, slobj, axis=0, kind=None):
        if axis == 0:
            new_index = self.index[slobj]
            new_columns = self.columns
        else:
            new_index = self.index
            new_columns = self.columns[slobj]

        return self.reindex(index=new_index, columns=new_columns)
