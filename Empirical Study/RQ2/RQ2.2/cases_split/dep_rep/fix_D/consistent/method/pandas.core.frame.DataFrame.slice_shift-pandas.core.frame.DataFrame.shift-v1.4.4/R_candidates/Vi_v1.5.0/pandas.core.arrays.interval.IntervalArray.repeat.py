    @Appender(_extension_array_shared_docs["repeat"] % _shared_docs_kwargs)
    def repeat(
        self: IntervalArrayT,
        repeats: int | Sequence[int],
        axis: int | None = None,
    ) -> IntervalArrayT:
        nv.validate_repeat((), {"axis": axis})
        left_repeat = self.left.repeat(repeats)
        right_repeat = self.right.repeat(repeats)
        return self._shallow_copy(left=left_repeat, right=right_repeat)
