    @_api.delete_parameter("3.6", "args")
    @_api.delete_parameter("3.6", "kwargs")
    def get_window_extent(self, renderer=None, *args, **kwargs):
        # docstring inherited
        return self.bbox
