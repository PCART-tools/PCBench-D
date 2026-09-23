    def transform_doc(self) -> bytes:
        """
        Parse stylesheet from file or buffer and run it.

        This method will parse stylesheet object into tree for parsing
        conditionally by its specific object type, then transforms
        original tree with XSLT script.
        """

        from lxml.etree import (
            XSLT,
            XMLParser,
            fromstring,
            parse,
        )

        style_doc = self.stylesheet

        handle_data = get_data_from_filepath(
            filepath_or_buffer=style_doc,
            encoding=self.encoding,
            compression=self.compression,
            storage_options=self.storage_options,
        )

        with preprocess_data(handle_data) as xml_data:
            curr_parser = XMLParser(encoding=self.encoding)

            if isinstance(xml_data, io.StringIO):
                xsl_doc = fromstring(
                    xml_data.getvalue().encode(self.encoding), parser=curr_parser
                )
            else:
                xsl_doc = parse(xml_data, parser=curr_parser)

        transformer = XSLT(xsl_doc)
        new_doc = transformer(self.root)

        return bytes(new_doc)
