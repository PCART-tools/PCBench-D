    def __iter__(self) -> Generator[Any, None, None]:
        if self.dtype in (List, Array):
            # TODO: either make a change and return py-native list data here, or find
            #  a faster way to return nested/List series; sequential 'get_index' calls
            #  make this path a lot slower (~10x) than it needs to be.
            get_index = self._s.get_index
            for idx in range(self.len()):
                yield get_index(idx)
        else:
            buffer_size = 25_000
            for offset in range(0, self.len(), buffer_size):
                yield from self.slice(offset, buffer_size).to_list()
