    def __getstate__(self):
        state = super().__getstate__()
        # We can't pickle the C Image cached object.
        state['_imcache'] = None
        return state
