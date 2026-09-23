class HandlerPathCollection(HandlerRegularPolyCollection):
    r"""Handler for `.PathCollection`\s, which are used by `~.Axes.scatter`."""
    def create_collection(self, orig_handle, sizes, offsets, transOffset):
        p = type(orig_handle)([orig_handle.get_paths()[0]],
                              sizes=sizes,
                              offsets=offsets,
                              transOffset=transOffset,
                              )
        return p
