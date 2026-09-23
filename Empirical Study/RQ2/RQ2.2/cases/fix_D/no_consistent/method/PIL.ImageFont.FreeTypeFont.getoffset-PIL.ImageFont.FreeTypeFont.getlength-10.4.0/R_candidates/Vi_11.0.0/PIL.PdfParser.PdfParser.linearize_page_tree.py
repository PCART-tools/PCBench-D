    def linearize_page_tree(
        self, node: PdfDict | None = None
    ) -> list[IndirectReference]:
        page_node = node if node is not None else self.page_tree_root
        check_format_condition(
            page_node[b"Type"] == b"Pages", "/Type of page tree node is not /Pages"
        )
        pages = []
        for kid in page_node[b"Kids"]:
            kid_object = self.read_indirect(kid)
            if kid_object[b"Type"] == b"Page":
                pages.append(kid)
            else:
                pages.extend(self.linearize_page_tree(node=kid_object))
        return pages
