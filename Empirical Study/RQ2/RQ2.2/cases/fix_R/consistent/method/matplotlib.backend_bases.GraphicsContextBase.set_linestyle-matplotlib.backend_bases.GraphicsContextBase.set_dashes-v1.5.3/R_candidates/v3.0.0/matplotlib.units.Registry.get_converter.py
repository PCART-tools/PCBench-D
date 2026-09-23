    def get_converter(self, x):
        """
        Get the converter for data that has the same type as *x*. If no
        converters are registered for *x*, returns ``None``.
        """

        if not len(self):
            return None  # nothing registered
        # DISABLED idx = id(x)
        # DISABLED cached = self._cached.get(idx)
        # DISABLED if cached is not None: return cached

        converter = None
        classx = getattr(x, '__class__', None)

        if classx is not None:
            converter = self.get(classx)

        if converter is None and hasattr(x, "values"):
            # this unpacks pandas series or dataframes...
            x = x.values

        # If x is an array, look inside the array for data with units
        if isinstance(x, np.ndarray) and x.size:
            xravel = x.ravel()
            try:
                # pass the first value of x that is not masked back to
                # get_converter
                if not np.all(xravel.mask):
                    # some elements are not masked
                    converter = self.get_converter(
                        xravel[np.argmin(xravel.mask)])
                    return converter
            except AttributeError:
                # not a masked_array
                # Make sure we don't recurse forever -- it's possible for
                # ndarray subclasses to continue to return subclasses and
                # not ever return a non-subclass for a single element.
                next_item = xravel[0]
                if (not isinstance(next_item, np.ndarray) or
                        next_item.shape != x.shape):
                    converter = self.get_converter(next_item)
                return converter

        # If we haven't found a converter yet, try to get the first element
        if converter is None:
            try:
                thisx = safe_first_element(x)
            except (TypeError, StopIteration):
                pass
            else:
                if classx and classx != getattr(thisx, '__class__', None):
                    converter = self.get_converter(thisx)
                    return converter

        # DISABLED self._cached[idx] = converter
        return converter
