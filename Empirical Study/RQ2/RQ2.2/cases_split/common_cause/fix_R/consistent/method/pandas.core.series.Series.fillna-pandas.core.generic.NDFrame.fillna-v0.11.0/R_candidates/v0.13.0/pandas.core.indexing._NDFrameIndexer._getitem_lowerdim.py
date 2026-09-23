    def _getitem_lowerdim(self, tup):

        ax0 = self.obj._get_axis(0)
        # a bit kludgy
        if isinstance(ax0, MultiIndex):
            try:
                return self._get_label(tup, axis=0)
            except TypeError:
                # slices are unhashable
                pass
            except Exception as e1:
                if isinstance(tup[0], (slice, Index)):
                    raise IndexingError

                # raise the error if we are not sorted
                if not ax0.is_lexsorted_for_tuple(tup):
                    raise e1
                try:
                    loc = ax0.get_loc(tup[0])
                except KeyError:
                    raise e1

        if len(tup) > self.obj.ndim:
            raise IndexingError

        # to avoid wasted computation
        # df.ix[d1:d2, 0] -> columns first (True)
        # df.ix[0, ['C', 'B', A']] -> rows first (False)
        for i, key in enumerate(tup):
            if _is_label_like(key) or isinstance(key, tuple):
                section = self._getitem_axis(key, axis=i)

                # we have yielded a scalar ?
                if not _is_list_like(section):
                    return section

                # might have been a MultiIndex
                elif section.ndim == self.ndim:

                    new_key = tup[:i] + (_NS,) + tup[i + 1:]

                else:
                    new_key = tup[:i] + tup[i + 1:]

                    # unfortunately need an odious kludge here because of
                    # DataFrame transposing convention
                    if (isinstance(section, ABCDataFrame) and i > 0
                            and len(new_key) == 2):
                        a, b = new_key
                        new_key = b, a

                    if len(new_key) == 1:
                        new_key, = new_key

                return getattr(section, self.name)[new_key]

        raise IndexingError('not applicable')
