    def _align_frame(self, indexer, df):
        is_frame = self.obj.ndim == 2
        is_panel = self.obj.ndim >= 3

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

            # panel
            if is_panel:

                # need to conform to the convention
                # as we are not selecting on the items axis
                # and we have a single indexer
                # GH 7763
                if len(sindexers) == 1 and sindexers[0] != 0:
                    df = df.T

                if idx is None:
                    idx = df.index
                if cols is None:
                    cols = df.columns

            if idx is not None and cols is not None:

                if df.index.equals(idx) and df.columns.equals(cols):
                    val = df.copy()._values
                else:
                    val = df.reindex(idx, columns=cols)._values
                return val

        elif ((isinstance(indexer, slice) or is_list_like_indexer(indexer)) and
              is_frame):
            ax = self.obj.index[indexer]
            if df.index.equals(ax):
                val = df.copy()._values
            else:

                # we have a multi-index and are trying to align
                # with a particular, level GH3738
                if (isinstance(ax, MultiIndex) and
                        isinstance(df.index, MultiIndex) and
                        ax.nlevels != df.index.nlevels):
                    raise TypeError("cannot align on a multi-index with out "
                                    "specifying the join levels")

                val = df.reindex(index=ax)._values
            return val

        elif is_scalar(indexer) and is_panel:
            idx = self.obj.axes[1]
            cols = self.obj.axes[2]

            # by definition we are indexing on the 0th axis
            # a passed in dataframe which is actually a transpose
            # of what is needed
            if idx.equals(df.index) and cols.equals(df.columns):
                return df.copy()._values

            return df.reindex(idx, columns=cols)._values

        raise ValueError('Incompatible indexer with DataFrame')
