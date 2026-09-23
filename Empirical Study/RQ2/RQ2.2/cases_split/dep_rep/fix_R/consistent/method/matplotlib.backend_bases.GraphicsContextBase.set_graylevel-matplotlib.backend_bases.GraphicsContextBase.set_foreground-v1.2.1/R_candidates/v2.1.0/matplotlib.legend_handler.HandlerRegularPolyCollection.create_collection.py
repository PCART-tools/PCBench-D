    def create_collection(self, orig_handle, sizes, offsets, transOffset):
        p = type(orig_handle)(orig_handle.get_numsides(),
                              rotation=orig_handle.get_rotation(),
                              sizes=sizes,
                              offsets=offsets,
                              transOffset=transOffset,
                              )
        return p
