    @_api.deprecated("3.4")
    def get_content_extents(self):
        orig_img = np.asarray(self.buffer_rgba())
        slice_y, slice_x = cbook._get_nonzero_slices(orig_img[..., 3])
        return (slice_x.start, slice_y.start,
                slice_x.stop - slice_x.start, slice_y.stop - slice_y.start)
