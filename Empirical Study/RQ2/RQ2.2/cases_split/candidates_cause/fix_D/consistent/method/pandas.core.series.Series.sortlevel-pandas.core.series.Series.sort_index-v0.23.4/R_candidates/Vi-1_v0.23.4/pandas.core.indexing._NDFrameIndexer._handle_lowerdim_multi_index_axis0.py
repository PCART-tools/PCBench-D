    def _handle_lowerdim_multi_index_axis0(self, tup):
        # we have an axis0 multi-index, handle or raise

        try:
            # fast path for series or for tup devoid of slices
            return self._get_label(tup, axis=self.axis)
        except TypeError:
            # slices are unhashable
            pass
        except Exception as e1:
            if isinstance(tup[0], (slice, Index)):
                raise IndexingError("Handle elsewhere")

            # raise the error if we are not sorted
            ax0 = self.obj._get_axis(0)
            if not ax0.is_lexsorted_for_tuple(tup):
                raise e1

        return None
