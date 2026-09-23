    def prettify_tree(self) -> bytes:
        """
        Output tree for pretty print format.

        This method will pretty print xml with line breaks and indentation.
        """

        from xml.dom.minidom import parseString

        dom = parseString(self.out_xml)

        return dom.toprettyxml(indent="  ", encoding=self.encoding)
