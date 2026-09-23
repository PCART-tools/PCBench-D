    def _align_frame(self, indexer, df: ABCDataFrame):
        is_frame = self.ndim == 2

        if isinstance(indexer, tuple):

            idx, cols = None, None
            sindexers = []
            for i, ix in enumerate(indexer):
                ax = self.obj.axes[i]
                if is_sequence(ix) or isinstance(ix, slice):
                    if isinstance(ix, np.ndarray):
                        ix = ix.ravel()
                    if idx is None:
                        idx = ax[ix]
                    elif cols is None:
                        cols = ax[ix]
                    else:
                        break
                else:
                    sindexers.append(i)

            if idx is not None and cols is not None:

                if df.index.equals(idx) and df.columns.equals(cols):
                    val = df.copy()._values
                else:
                    val = df.reindex(idx, columns=cols)._values
                return val

        elif (isinstance(indexer, slice) or is_list_like_indexer(indexer)) and is_frame:
            ax = self.obj.index[indexer]
            if df.index.equals(ax):
                val = df.copy()._values
            else:

                # we have a multi-index and are trying to align
                # with a particular, level GH3738
                if (
                    isinstance(ax, ABCMultiIndex)
                    and isinstance(df.index, ABCMultiIndex)
                    and ax.nlevels != df.index.nlevels
                ):
                    raise TypeError(
                        "cannot align on a multi-index with out "
                        "specifying the join levels"
                    )

                val = df.reindex(index=ax)._values
            return val

        raise ValueError("Incompatible indexer with DataFrame")
