    def __new__(cls, idx_obj, pspace=None):
        if not isinstance(idx_obj, (Indexed, Function)):
            raise TypeError("An Function or Indexed object is expected not %s"%(idx_obj))
        return Basic.__new__(cls, idx_obj, pspace)
