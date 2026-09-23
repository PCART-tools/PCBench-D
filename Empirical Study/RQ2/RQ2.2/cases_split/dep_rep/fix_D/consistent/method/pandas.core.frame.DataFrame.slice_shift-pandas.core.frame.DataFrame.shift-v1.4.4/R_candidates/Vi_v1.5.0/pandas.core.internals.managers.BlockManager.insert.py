    def insert(self, loc: int, item: Hashable, value: ArrayLike) -> None:
        """
        Insert item at selected position.

        Parameters
        ----------
        loc : int
        item : hashable
        value : np.ndarray or ExtensionArray
        """
        # insert to the axis; this could possibly raise a TypeError
        new_axis = self.items.insert(loc, item)

        if value.ndim == 2:
            value = value.T
            if len(value) > 1:
                raise ValueError(
                    f"Expected a 1D array, got an array with shape {value.T.shape}"
                )
        else:
            value = ensure_block_shape(value, ndim=self.ndim)

        bp = BlockPlacement(slice(loc, loc + 1))
        block = new_block_2d(values=value, placement=bp)

        if not len(self.blocks):
            # Fastpath
            self._blklocs = np.array([0], dtype=np.intp)
            self._blknos = np.array([0], dtype=np.intp)
        else:
            self._insert_update_mgr_locs(loc)
            self._insert_update_blklocs_and_blknos(loc)

        self.axes[0] = new_axis
        self.blocks += (block,)
        # TODO(CoW) do we always "own" the passed `value`?
        if self.refs is not None:
            self.refs += [None]

        self._known_consolidated = False

        if sum(not block.is_extension for block in self.blocks) > 100:
            warnings.warn(
                "DataFrame is highly fragmented.  This is usually the result "
                "of calling `frame.insert` many times, which has poor performance.  "
                "Consider joining all columns at once using pd.concat(axis=1) "
                "instead. To get a de-fragmented frame, use `newframe = frame.copy()`",
                PerformanceWarning,
                stacklevel=find_stack_level(inspect.currentframe()),
            )
