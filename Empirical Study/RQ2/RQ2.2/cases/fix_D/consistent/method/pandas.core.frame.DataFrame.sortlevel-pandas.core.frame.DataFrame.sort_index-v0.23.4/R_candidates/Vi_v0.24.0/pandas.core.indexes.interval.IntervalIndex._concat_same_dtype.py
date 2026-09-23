    def _concat_same_dtype(self, to_concat, name):
        """
        assert that we all have the same .closed
        we allow a 0-len index here as well
        """
        if not len({i.closed for i in to_concat if len(i)}) == 1:
            msg = ('can only append two IntervalIndex objects '
                   'that are closed on the same side')
            raise ValueError(msg)
        return super(IntervalIndex, self)._concat_same_dtype(to_concat, name)
