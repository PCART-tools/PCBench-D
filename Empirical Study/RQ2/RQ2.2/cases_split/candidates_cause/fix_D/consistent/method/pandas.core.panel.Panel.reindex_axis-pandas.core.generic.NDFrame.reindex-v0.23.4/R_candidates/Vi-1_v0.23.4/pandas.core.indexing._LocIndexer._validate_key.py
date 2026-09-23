    @Appender(_NDFrameIndexer._validate_key.__doc__)
    def _validate_key(self, key, axis):
        ax = self.obj._get_axis(axis)

        # valid for a label where all labels are in the index
        # slice of labels (where start-end in labels)
        # slice of integers (only if in the labels)
        # boolean

        if isinstance(key, slice):
            return

        elif com.is_bool_indexer(key):
            return

        elif not is_list_like_indexer(key):

            def error():
                if isna(key):
                    raise TypeError("cannot use label indexing with a null "
                                    "key")
                raise KeyError(u"the label [{key}] is not in the [{axis}]"
                               .format(key=key,
                                       axis=self.obj._get_axis_name(axis)))

            try:
                key = self._convert_scalar_indexer(key, axis)
                if not ax.contains(key):
                    error()
            except TypeError as e:

                # python 3 type errors should be raised
                if _is_unorderable_exception(e):
                    error()
                raise
            except:
                error()
