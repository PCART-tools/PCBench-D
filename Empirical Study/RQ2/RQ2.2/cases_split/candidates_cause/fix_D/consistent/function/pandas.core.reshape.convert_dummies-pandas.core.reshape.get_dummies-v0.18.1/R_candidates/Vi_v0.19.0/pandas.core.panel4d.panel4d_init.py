def panel4d_init(self, data=None, labels=None, items=None, major_axis=None,
                 minor_axis=None, copy=False, dtype=None):

    # deprecation GH13564
    warnings.warn("\nPanel4D is deprecated and will be removed in a "
                  "future version.\nThe recommended way to represent "
                  "these types of n-dimensional data are with\n"
                  "the `xarray package "
                  "<http://xarray.pydata.org/en/stable/>`__.\n"
                  "Pandas provides a `.to_xarray()` method to help "
                  "automate this conversion.\n",
                  FutureWarning, stacklevel=2)
    self._init_data(data=data, labels=labels, items=items,
                    major_axis=major_axis, minor_axis=minor_axis, copy=copy,
                    dtype=dtype)
