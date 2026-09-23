    def _join_compat(self, other, on=None, how='left', lsuffix='', rsuffix='',
                     sort=False):
        from pandas.tools.merge import merge, concat

        if isinstance(other, Series):
            if other.name is None:
                raise ValueError('Other Series must have a name')
            other = DataFrame({other.name: other})

        if isinstance(other, DataFrame):
            return merge(self, other, left_on=on, how=how,
                         left_index=on is None, right_index=True,
                         suffixes=(lsuffix, rsuffix), sort=sort)
        else:
            if on is not None:
                raise ValueError('Joining multiple DataFrames only supported'
                                 ' for joining on index')

            # join indexes only using concat
            if how == 'left':
                how = 'outer'
                join_axes = [self.index]
            else:
                join_axes = None

            frames = [self] + list(other)

            can_concat = all(df.index.is_unique for df in frames)

            if can_concat:
                return concat(frames, axis=1, join=how, join_axes=join_axes,
                              verify_integrity=True)

            joined = frames[0]

            for frame in frames[1:]:
                joined = merge(joined, frame, how=how, left_index=True,
                               right_index=True)

            return joined
