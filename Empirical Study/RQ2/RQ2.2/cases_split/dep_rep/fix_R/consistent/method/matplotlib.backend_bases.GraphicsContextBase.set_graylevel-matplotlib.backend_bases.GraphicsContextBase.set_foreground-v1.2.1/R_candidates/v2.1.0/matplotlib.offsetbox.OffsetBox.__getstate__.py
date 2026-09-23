    def __getstate__(self):
        state = martist.Artist.__getstate__(self)

        # pickle cannot save instancemethods, so handle them here
        from .cbook import _InstanceMethodPickler
        import inspect

        offset = state['_offset']
        if inspect.ismethod(offset):
            state['_offset'] = _InstanceMethodPickler(offset)
        return state
