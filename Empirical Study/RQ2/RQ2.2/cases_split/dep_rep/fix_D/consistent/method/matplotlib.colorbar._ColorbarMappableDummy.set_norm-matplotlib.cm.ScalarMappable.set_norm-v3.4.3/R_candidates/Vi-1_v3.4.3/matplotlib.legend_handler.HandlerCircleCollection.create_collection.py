    def create_collection(self, orig_handle, sizes, offsets, transOffset):
        p = type(orig_handle)(sizes,
                              offsets=offsets,
                              transOffset=transOffset,
                              )
        return p
