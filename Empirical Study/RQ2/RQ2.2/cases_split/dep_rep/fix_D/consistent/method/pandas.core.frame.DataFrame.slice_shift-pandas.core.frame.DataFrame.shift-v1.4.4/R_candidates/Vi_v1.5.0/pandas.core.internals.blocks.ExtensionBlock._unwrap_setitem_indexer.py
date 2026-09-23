    def _unwrap_setitem_indexer(self, indexer):
        """
        Adapt a 2D-indexer to our 1D values.

        This is intended for 'setitem', not 'iget' or '_slice'.
        """
        # TODO: ATM this doesn't work for iget/_slice, can we change that?

        if isinstance(indexer, tuple):
            # TODO(EA2D): not needed with 2D EAs
            #  Should never have length > 2.  Caller is responsible for checking.
            #  Length 1 is reached vis setitem_single_block and setitem_single_column
            #  each of which pass indexer=(pi,)
            if len(indexer) == 2:

                if all(isinstance(x, np.ndarray) and x.ndim == 2 for x in indexer):
                    # GH#44703 went through indexing.maybe_convert_ix
                    first, second = indexer
                    if not (
                        second.size == 1 and (second == 0).all() and first.shape[1] == 1
                    ):
                        raise NotImplementedError(
                            "This should not be reached. Please report a bug at "
                            "github.com/pandas-dev/pandas/"
                        )
                    indexer = first[:, 0]

                elif lib.is_integer(indexer[1]) and indexer[1] == 0:
                    # reached via setitem_single_block passing the whole indexer
                    indexer = indexer[0]

                elif com.is_null_slice(indexer[1]):
                    indexer = indexer[0]

                elif is_list_like(indexer[1]) and indexer[1][0] == 0:
                    indexer = indexer[0]

                else:
                    raise NotImplementedError(
                        "This should not be reached. Please report a bug at "
                        "github.com/pandas-dev/pandas/"
                    )
        return indexer
