    def build_elems(self, d: dict[str, Any], elem_row: Any) -> None:
        from xml.etree.ElementTree import SubElement

        self._build_elems(SubElement, d, elem_row)
