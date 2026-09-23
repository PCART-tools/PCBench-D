    def _align_frame(self, indexer, df):
        is_frame = self.obj.ndim == 2
        is_panel = self.obj.ndim >= 3

        if isinstance(indexer, tuple):

            aligners = [not _is_null_slice(idx) for idx in indexer]
            sum_aligners = sum(aligners)
            single_aligner = sum_aligners == 1

            idx, cols = None, None
            sindexers = []
            for i, ix in enumerate(indexer):
                ax = self.obj.axes[i]
                if com._is_sequence(ix) or isinstance(ix, slice):
                    if idx is None:
                        idx = ax[ix].ravel()
                    elif cols is None:
                        cols = ax[ix].ravel()
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
                    val = df.copy().values
                else:
                    val = df.reindex(idx, columns=cols).values
                return val

        elif ((isinstance(indexer, slice) or com.is_list_like(indexer))
              and is_frame):
            ax = self.obj.index[indexer]
            if df.index.equals(ax):
                val = df.copy().values
            else:

                # we have a multi-index and are trying to align
                # with a particular, level GH3738
                if isinstance(ax, MultiIndex) and isinstance(
                    df.index, MultiIndex) and ax.nlevels != df.index.nlevels:
                    raise TypeError("cannot align on a multi-index with out specifying the join levels")

                val = df.reindex(index=ax).values
            return val

        elif np.isscalar(indexer) and is_panel:
            idx = self.obj.axes[1]
            cols = self.obj.axes[2]

            # by definition we are indexing on the 0th axis
            # a passed in dataframe which is actually a transpose
            # of what is needed
            if idx.equals(df.index) and cols.equals(df.columns):
                return df.copy().values

            return df.reindex(idx, columns=cols).values

        raise ValueError('Incompatible indexer with DataFrame')
