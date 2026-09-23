    def _join_multi(self, other, how, return_indexers=True):
        from .multi import MultiIndex
        self_is_mi = isinstance(self, MultiIndex)
        other_is_mi = isinstance(other, MultiIndex)

        # figure out join names
        self_names = com._not_none(*self.names)
        other_names = com._not_none(*other.names)
        overlap = list(set(self_names) & set(other_names))

        # need at least 1 in common, but not more than 1
        if not len(overlap):
            raise ValueError("cannot join with no level specified and no "
                             "overlapping names")
        if len(overlap) > 1:
            raise NotImplementedError("merging with more than one level "
                                      "overlap on a multi-index is not "
                                      "implemented")
        jl = overlap[0]

        # make the indices into mi's that match
        if not (self_is_mi and other_is_mi):

            flip_order = False
            if self_is_mi:
                self, other = other, self
                flip_order = True
                # flip if join method is right or left
                how = {'right': 'left', 'left': 'right'}.get(how, how)

            level = other.names.index(jl)
            result = self._join_level(other, level, how=how,
                                      return_indexers=return_indexers)

            if flip_order:
                if isinstance(result, tuple):
                    return result[0], result[2], result[1]
            return result

        # 2 multi-indexes
        raise NotImplementedError("merging with both multi-indexes is not "
                                  "implemented")
