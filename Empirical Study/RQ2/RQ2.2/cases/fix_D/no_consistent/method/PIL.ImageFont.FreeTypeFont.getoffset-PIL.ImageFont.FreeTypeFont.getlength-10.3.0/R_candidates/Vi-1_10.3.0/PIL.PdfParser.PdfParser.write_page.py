    def write_page(self, ref, *objs, **dict_obj):
        if isinstance(ref, int):
            ref = self.pages[ref]
        if "Type" not in dict_obj:
            dict_obj["Type"] = PdfName(b"Page")
        if "Parent" not in dict_obj:
            dict_obj["Parent"] = self.pages_ref
        return self.write_obj(ref, *objs, **dict_obj)
