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
            self.d = d
            self.elem_row = SubElement(self.root, f"{self.prefix_uri}{self.row_name}")

            if not self.attr_cols and not self.elem_cols:
                self.elem_cols = list(self.d.keys())
                self.build_elems()

            else:
                self.build_attribs()
                self.build_elems()

        self.out_xml = tostring(self.root, method="xml", encoding=self.encoding)

        if self.pretty_print:
            self.out_xml = self.prettify_tree()

        if self.xml_declaration:
            self.out_xml = self.add_declaration()
        else:
            self.out_xml = self.remove_declaration()

        if self.stylesheet is not None:
            raise ValueError(
                "To use stylesheet, you need lxml installed and selected as parser."
            )

        return self.out_xml
