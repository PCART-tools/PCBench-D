    def __getstate__(self):
        d = super(Text, self).__getstate__()
        # remove the cached _renderer (if it exists)
        d['_renderer'] = None
        return d
