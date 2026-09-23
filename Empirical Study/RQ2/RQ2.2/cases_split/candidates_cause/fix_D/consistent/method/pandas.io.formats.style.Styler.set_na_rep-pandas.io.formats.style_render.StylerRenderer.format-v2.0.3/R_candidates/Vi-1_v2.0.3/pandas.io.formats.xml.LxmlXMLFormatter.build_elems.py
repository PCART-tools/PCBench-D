    def build_elems(self, d: dict[str, Any], elem_row: Any) -> None:
        from lxml.etree import SubElement

        self._build_elems(SubElement, d, elem_row)
