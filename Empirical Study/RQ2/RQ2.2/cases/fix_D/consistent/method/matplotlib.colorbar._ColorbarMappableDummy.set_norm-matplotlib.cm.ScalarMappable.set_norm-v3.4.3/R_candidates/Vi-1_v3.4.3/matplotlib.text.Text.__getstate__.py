    def __getstate__(self):
        d = super().__getstate__()
        # remove the cached _renderer (if it exists)
        d['_renderer'] = None
        return d
