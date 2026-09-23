    def build_tree(self) -> bytes:
        from xml.etree.ElementTree import (
            Element,
            SubElement,
            tostring,
        )

        self.root = Element(
            f"{self.prefix_uri}{self.root_name}", attrib=self.other_namespaces()
        )

        for d in self.frame_dicts.values():
            elem_row = SubElement(self.root, f"{self.prefix_uri}{self.row_name}")

            if not self.attr_cols and not self.elem_cols:
                self.elem_cols = list(d.keys())
                self.build_elems(d, elem_row)

            else:
                elem_row = self.build_attribs(d, elem_row)
                self.build_elems(d, elem_row)

        self.out_xml = tostring(
            self.root,
            method="xml",
            encoding=self.encoding,
            xml_declaration=self.xml_declaration,
        )

        if self.pretty_print:
            self.out_xml = self.prettify_tree()

        if self.stylesheet is not None:
            raise ValueError(
                "To use stylesheet, you need lxml installed and selected as parser."
            )

        return self.out_xml
