    def __getstate__(self):
        # The renderer should be re-created by the figure, and then cached at
        # that point.
        state = super(_AxesBase, self).__getstate__()
        state['_cachedRenderer'] = None
        return state
