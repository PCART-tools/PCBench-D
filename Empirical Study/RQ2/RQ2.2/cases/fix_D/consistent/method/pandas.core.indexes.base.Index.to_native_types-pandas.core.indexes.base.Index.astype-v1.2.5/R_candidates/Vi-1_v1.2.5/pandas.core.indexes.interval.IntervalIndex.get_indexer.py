    @Substitution(
        **dict(
            _index_doc_kwargs,
            **{
                "raises_section": textwrap.dedent(
                    """
        Raises
        ------
        NotImplementedError
            If any method argument other than the default of
            None is specified as these are not yet implemented.
        """
                )
            },
        )
    )
    @Appender(_index_shared_docs["get_indexer"])
    def get_indexer(
        self,
        target: AnyArrayLike,
        method: Optional[str] = None,
        limit: Optional[int] = None,
        tolerance: Optional[Any] = None,
    ) -> np.ndarray:

        self._check_indexing_method(method)

        if self.is_overlapping:
            raise InvalidIndexError(
                "cannot handle overlapping indices; "
                "use IntervalIndex.get_indexer_non_unique"
            )

        target_as_index = ensure_index(target)

        if isinstance(target_as_index, IntervalIndex):
            # equal indexes -> 1:1 positional match
            if self.equals(target_as_index):
                return np.arange(len(self), dtype="intp")

            if self._is_non_comparable_own_type(target_as_index):
                # different closed or incompatible subtype -> no matches
                return np.repeat(np.intp(-1), len(target_as_index))

            # non-overlapping -> at most one match per interval in target_as_index
            # want exact matches -> need both left/right to match, so defer to
            # left/right get_indexer, compare elementwise, equality -> match
            left_indexer = self.left.get_indexer(target_as_index.left)
            right_indexer = self.right.get_indexer(target_as_index.right)
            indexer = np.where(left_indexer == right_indexer, left_indexer, -1)
        elif is_categorical_dtype(target_as_index.dtype):
            target_as_index = cast("CategoricalIndex", target_as_index)
            # get an indexer for unique categories then propagate to codes via take_1d
            categories_indexer = self.get_indexer(target_as_index.categories)
            indexer = take_1d(categories_indexer, target_as_index.codes, fill_value=-1)
        elif not is_object_dtype(target_as_index):
            # homogeneous scalar index: use IntervalTree
            target_as_index = self._maybe_convert_i8(target_as_index)
            indexer = self._engine.get_indexer(target_as_index.values)
        else:
            # heterogeneous scalar index: defer elementwise to get_loc
            return self._get_indexer_pointwise(target_as_index)[0]

        return ensure_platform_int(indexer)
