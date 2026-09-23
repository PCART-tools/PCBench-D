    def remove_declaration(self) -> bytes:
        """
        Remove xml declaration.

        This method will remove xml declaration of working tree. Currently,
        pretty_print is not supported in etree.
        """

        return self.out_xml.split(b"?>")[-1].strip()
