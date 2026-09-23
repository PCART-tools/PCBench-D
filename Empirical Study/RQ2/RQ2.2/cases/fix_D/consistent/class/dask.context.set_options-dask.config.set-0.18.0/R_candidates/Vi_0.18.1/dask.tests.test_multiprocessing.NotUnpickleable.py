class NotUnpickleable(object):
    def __getstate__(self):
        return ()

    def __setstate__(self, state):
        raise ValueError("Can't unpickle me")
