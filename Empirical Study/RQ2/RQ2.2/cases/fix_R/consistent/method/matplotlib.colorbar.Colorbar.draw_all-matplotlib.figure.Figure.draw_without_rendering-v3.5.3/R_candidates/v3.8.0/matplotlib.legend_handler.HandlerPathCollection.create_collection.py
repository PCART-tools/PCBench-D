    def create_collection(self, orig_handle, sizes, offsets, offset_transform):
        return type(orig_handle)(
            [orig_handle.get_paths()[0]], sizes=sizes,
            offsets=offsets, offset_transform=offset_transform,
        )
