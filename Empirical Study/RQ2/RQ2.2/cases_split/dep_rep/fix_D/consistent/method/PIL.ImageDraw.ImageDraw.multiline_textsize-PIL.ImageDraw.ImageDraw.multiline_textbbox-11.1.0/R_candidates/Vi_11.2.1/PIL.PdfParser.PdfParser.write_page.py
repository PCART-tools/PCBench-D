    def write_page(
        self, ref: int | IndirectReference | None, *objs: Any, **dict_obj: Any
    ) -> IndirectReference:
        obj_ref = self.pages[ref] if isinstance(ref, int) else ref
        if "Type" not in dict_obj:
            dict_obj["Type"] = PdfName(b"Page")
        if "Parent" not in dict_obj:
            dict_obj["Parent"] = self.pages_ref
        return self.write_obj(obj_ref, *objs, **dict_obj)
