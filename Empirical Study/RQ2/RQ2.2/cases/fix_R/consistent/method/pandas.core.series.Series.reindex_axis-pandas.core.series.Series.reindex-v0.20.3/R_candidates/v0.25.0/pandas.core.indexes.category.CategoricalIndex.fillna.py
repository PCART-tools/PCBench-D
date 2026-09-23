    @Appender(ibase._index_shared_docs["fillna"])
    def fillna(self, value, downcast=None):
        self._assert_can_do_op(value)
        return CategoricalIndex(self._data.fillna(value), name=self.name)
