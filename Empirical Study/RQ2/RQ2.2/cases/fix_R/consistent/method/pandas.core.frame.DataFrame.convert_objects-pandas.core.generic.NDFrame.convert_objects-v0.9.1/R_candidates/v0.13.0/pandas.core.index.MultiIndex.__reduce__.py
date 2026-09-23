    def __reduce__(self):
        """Necessary for making this object picklable"""
        object_state = list(np.ndarray.__reduce__(self))
        subclass_state = ([lev.view(np.ndarray) for lev in self.levels],
                          [label.view(np.ndarray) for label in self.labels],
                          self.sortorder, list(self.names))
        object_state[2] = (object_state[2], subclass_state)
        return tuple(object_state)
