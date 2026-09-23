    @doc(NDFrame.shift, klass=_shared_doc_kwargs["klass"])
    def shift(
        self,
        periods: int | Sequence[int] = 1,
        freq: Frequency | None = None,
        axis: Axis = 0,
        fill_value: Hashable = lib.no_default,
        suffix: str | None = None,
    ) -> DataFrame:
        if freq is not None and fill_value is not lib.no_default:
            # GH#53832
            warnings.warn(
                "Passing a 'freq' together with a 'fill_value' silently ignores "
                "the fill_value and is deprecated. This will raise in a future "
                "version.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
            fill_value = lib.no_default

        axis = self._get_axis_number(axis)

        if is_list_like(periods):
            periods = cast(Sequence, periods)
            if axis == 1:
                raise ValueError(
                    "If `periods` contains multiple shifts, `axis` cannot be 1."
                )
            if len(periods) == 0:
                raise ValueError("If `periods` is an iterable, it cannot be empty.")
            from pandas.core.reshape.concat import concat

            shifted_dataframes = []
            for period in periods:
                if not is_integer(period):
                    raise TypeError(
                        f"Periods must be integer, but {period} is {type(period)}."
                    )
                period = cast(int, period)
                shifted_dataframes.append(
                    super()
                    .shift(periods=period, freq=freq, axis=axis, fill_value=fill_value)
                    .add_suffix(f"{suffix}_{period}" if suffix else f"_{period}")
                )
            return concat(shifted_dataframes, axis=1)
        elif suffix:
            raise ValueError("Cannot specify `suffix` if `periods` is an int.")
        periods = cast(int, periods)

        ncols = len(self.columns)
        arrays = self._mgr.arrays
        if axis == 1 and periods != 0 and ncols > 0 and freq is None:
            if fill_value is lib.no_default:
                # We will infer fill_value to match the closest column

                # Use a column that we know is valid for our column's dtype GH#38434
                label = self.columns[0]

                if periods > 0:
                    result = self.iloc[:, :-periods]
                    for col in range(min(ncols, abs(periods))):
                        # TODO(EA2D): doing this in a loop unnecessary with 2D EAs
                        # Define filler inside loop so we get a copy
                        filler = self.iloc[:, 0].shift(len(self))
                        result.insert(0, label, filler, allow_duplicates=True)
                else:
                    result = self.iloc[:, -periods:]
                    for col in range(min(ncols, abs(periods))):
                        # Define filler inside loop so we get a copy
                        filler = self.iloc[:, -1].shift(len(self))
                        result.insert(
                            len(result.columns), label, filler, allow_duplicates=True
                        )

                result.columns = self.columns.copy()
                return result
            elif len(arrays) > 1 or (
                # If we only have one block and we know that we can't
                #  keep the same dtype (i.e. the _can_hold_element check)
                #  then we can go through the reindex_indexer path
                #  (and avoid casting logic in the Block method).
                not can_hold_element(arrays[0], fill_value)
            ):
                # GH#35488 we need to watch out for multi-block cases
                # We only get here with fill_value not-lib.no_default
                nper = abs(periods)
                nper = min(nper, ncols)
                if periods > 0:
                    indexer = np.array(
                        [-1] * nper + list(range(ncols - periods)), dtype=np.intp
                    )
                else:
                    indexer = np.array(
                        list(range(nper, ncols)) + [-1] * nper, dtype=np.intp
                    )
                mgr = self._mgr.reindex_indexer(
                    self.columns,
                    indexer,
                    axis=0,
                    fill_value=fill_value,
                    allow_dups=True,
                )
                res_df = self._constructor_from_mgr(mgr, axes=mgr.axes)
                return res_df.__finalize__(self, method="shift")
            else:
                return self.T.shift(periods=periods, fill_value=fill_value).T

        return super().shift(
            periods=periods, freq=freq, axis=axis, fill_value=fill_value
        )
