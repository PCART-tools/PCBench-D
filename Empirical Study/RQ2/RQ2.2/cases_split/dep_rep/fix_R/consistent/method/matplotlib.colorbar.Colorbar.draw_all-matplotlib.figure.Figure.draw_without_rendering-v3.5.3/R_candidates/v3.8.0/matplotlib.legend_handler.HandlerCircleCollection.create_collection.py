    def create_collection(self, orig_handle, sizes, offsets, offset_transform):
        return type(orig_handle)(
            sizes, offsets=offsets, offset_transform=offset_transform)
