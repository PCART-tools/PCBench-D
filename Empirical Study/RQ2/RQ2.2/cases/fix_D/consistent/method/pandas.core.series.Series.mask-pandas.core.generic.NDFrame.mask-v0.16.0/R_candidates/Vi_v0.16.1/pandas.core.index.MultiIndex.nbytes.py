    @cache_readonly
    def nbytes(self):
        """ return the number of bytes in the underlying data """
        level_nbytes = sum(( i.nbytes for i in self.levels ))
        label_nbytes = sum(( i.nbytes for i in self.labels ))
        names_nbytes = sum(( getsizeof(i) for i in self.names ))
        return level_nbytes + label_nbytes + names_nbytes
