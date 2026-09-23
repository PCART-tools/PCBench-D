    def __init__(self, data=None, items=None, major_axis=None, minor_axis=None,
                 copy=False, dtype=None):
        # deprecation GH13563
        warnings.warn("\nPanel is deprecated and will be removed in a "
                      "future version.\nThe recommended way to represent "
                      "these types of 3-dimensional data are with a "
                      "MultiIndex on a DataFrame, via the "
                      "Panel.to_frame() method\n"
                      "Alternatively, you can use the xarray package "
                      "http://xarray.pydata.org/en/stable/.\n"
                      "Pandas provides a `.to_xarray()` method to help "
                      "automate this conversion.\n",
                      DeprecationWarning, stacklevel=3)

        self._init_data(data=data, items=items, major_axis=major_axis,
                        minor_axis=minor_axis, copy=copy, dtype=dtype)
