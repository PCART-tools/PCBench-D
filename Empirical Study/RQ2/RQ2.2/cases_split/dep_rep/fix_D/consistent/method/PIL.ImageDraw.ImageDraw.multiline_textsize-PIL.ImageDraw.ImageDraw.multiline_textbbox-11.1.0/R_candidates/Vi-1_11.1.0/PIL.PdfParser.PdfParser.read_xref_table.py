    def read_xref_table(self, xref_section_offset: int) -> int:
        assert self.buf is not None
        subsection_found = False
        m = self.re_xref_section_start.match(
            self.buf, xref_section_offset + self.start_offset
        )
        check_format_condition(m is not None, "xref section start not found")
        assert m is not None
        offset = m.end()
        while True:
            m = self.re_xref_subsection_start.match(self.buf, offset)
            if not m:
                check_format_condition(
                    subsection_found, "xref subsection start not found"
                )
                break
            subsection_found = True
            offset = m.end()
            first_object = int(m.group(1))
            num_objects = int(m.group(2))
            for i in range(first_object, first_object + num_objects):
                m = self.re_xref_entry.match(self.buf, offset)
                check_format_condition(m is not None, "xref entry not found")
                assert m is not None
                offset = m.end()
                is_free = m.group(3) == b"f"
                if not is_free:
                    generation = int(m.group(2))
                    new_entry = (int(m.group(1)), generation)
                    if i not in self.xref_table:
                        self.xref_table[i] = new_entry
        return offset
