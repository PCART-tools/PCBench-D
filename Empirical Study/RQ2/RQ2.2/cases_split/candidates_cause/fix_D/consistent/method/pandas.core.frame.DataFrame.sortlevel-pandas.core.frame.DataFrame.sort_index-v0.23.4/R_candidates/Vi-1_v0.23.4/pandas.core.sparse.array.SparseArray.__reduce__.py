    def __reduce__(self):
        """Necessary for making this object picklable"""
        object_state = list(np.ndarray.__reduce__(self))
        subclass_state = self.fill_value, self.sp_index
        object_state[2] = self.sp_values.__reduce__()[2]
        object_state[2] = (object_state[2], subclass_state)
        return tuple(object_state)
