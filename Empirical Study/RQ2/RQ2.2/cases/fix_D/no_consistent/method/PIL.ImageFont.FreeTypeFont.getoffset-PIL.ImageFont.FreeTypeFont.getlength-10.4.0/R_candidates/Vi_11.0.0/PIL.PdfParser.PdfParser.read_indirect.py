    def read_indirect(self, ref: IndirectReference, max_nesting: int = -1) -> Any:
        offset, generation = self.xref_table[ref[0]]
        check_format_condition(
            generation == ref[1],
            f"expected to find generation {ref[1]} for object ID {ref[0]} in xref "
            f"table, instead found generation {generation} at offset {offset}",
        )
        assert self.buf is not None
        value = self.get_value(
            self.buf,
            offset + self.start_offset,
            expect_indirect=IndirectReference(*ref),
            max_nesting=max_nesting,
        )[0]
        self.cached_objects[ref] = value
        return value
