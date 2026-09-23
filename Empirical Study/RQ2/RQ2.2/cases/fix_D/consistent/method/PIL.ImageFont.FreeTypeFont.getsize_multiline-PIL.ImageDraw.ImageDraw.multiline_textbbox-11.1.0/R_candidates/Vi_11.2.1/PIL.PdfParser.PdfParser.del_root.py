    def del_root(self) -> None:
        if self.root_ref is None:
            return
        del self.xref_table[self.root_ref.object_id]
        del self.xref_table[self.root[b"Pages"].object_id]
