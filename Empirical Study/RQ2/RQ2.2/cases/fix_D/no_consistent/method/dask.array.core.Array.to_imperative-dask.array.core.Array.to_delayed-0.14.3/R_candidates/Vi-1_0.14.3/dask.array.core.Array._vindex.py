    def _vindex(self, key):
        if (not isinstance(key, tuple) or
           not len([k for k in key if isinstance(k, (np.ndarray, list))]) >= 2 or
           not all(isinstance(k, (np.ndarray, list)) or k == slice(None, None)
                   for k in key)):
            msg = ("vindex expects only lists and full slices\n"
                   "At least two entries must be a list\n"
                   "For other combinations try doing normal slicing first, followed\n"
                   "by vindex slicing.  Got: \n\t%s")
            raise IndexError(msg % str(key))
        if any((isinstance(k, np.ndarray) and k.ndim != 1) or
               (isinstance(k, list) and k and isinstance(k[0], list))
               for k in key):
            raise IndexError("vindex does not support multi-dimensional keys\n"
                             "Got: %s" % str(key))
        if len(set(len(k) for k in key if isinstance(k, (list, np.ndarray)))) != 1:
            raise IndexError("All indexers must have the same length, got\n"
                             "\t%s" % str(key))
        key = key + (slice(None, None),) * (self.ndim - len(key))
        key = [i if isinstance(i, list) else
               i.tolist() if isinstance(i, np.ndarray) else
               None for i in key]
        return _vindex(self, *key)
