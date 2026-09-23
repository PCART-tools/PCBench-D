    def set_locs(self, locs):
        self.locs = np.array(locs)
        self._labelled.clear()

        if not self._minor:
            return None
        if all(
            is_decade(x, rtol=1e-7)
            or is_decade(1 - x, rtol=1e-7)
            or (is_close_to_int(2 * x) and int(np.round(2 * x)) == 1)
            for x in locs
        ):
            # minor ticks are subsample from ideal, so no label
            return None
        if len(locs) < self._minor_threshold:
            if len(locs) < self._minor_number:
                self._labelled.update(locs)
            else:
                # we do not have a lot of minor ticks, so only few decades are
                # displayed, then we choose some (spaced) minor ticks to label.
                # Only minor ticks are known, we assume it is sufficient to
                # choice which ticks are displayed.
                # For each ticks we compute the distance between the ticks and
                # the previous, and between the ticks and the next one. Ticks
                # with smallest minimum are chosen. As tiebreak, the ticks
                # with smallest sum is chosen.
                diff = np.diff(-np.log(1 / self.locs - 1))
                space_pessimistic = np.minimum(
                    np.concatenate(((np.inf,), diff)),
                    np.concatenate((diff, (np.inf,))),
                )
                space_sum = (
                    np.concatenate(((0,), diff))
                    + np.concatenate((diff, (0,)))
                )
                good_minor = sorted(
                    range(len(self.locs)),
                    key=lambda i: (space_pessimistic[i], space_sum[i]),
                )[-self._minor_number:]
                self._labelled.update(locs[i] for i in good_minor)
