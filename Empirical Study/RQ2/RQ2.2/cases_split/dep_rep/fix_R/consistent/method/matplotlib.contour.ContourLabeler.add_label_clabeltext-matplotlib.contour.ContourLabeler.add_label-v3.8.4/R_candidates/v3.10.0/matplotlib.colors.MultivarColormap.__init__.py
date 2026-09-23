    def __init__(self, colormaps, combination_mode, name='multivariate colormap'):
        """
        Parameters
        ----------
        colormaps: list or tuple of `~matplotlib.colors.Colormap` objects
            The individual colormaps that are combined
        combination_mode: str, 'sRGB_add' or 'sRGB_sub'
            Describe how colormaps are combined in sRGB space

            - If 'sRGB_add' -> Mixing produces brighter colors
              `sRGB = sum(colors)`
            - If 'sRGB_sub' -> Mixing produces darker colors
              `sRGB = 1 - sum(1 - colors)`
        name : str, optional
            The name of the colormap family.
        """
        self.name = name

        if not np.iterable(colormaps) \
           or len(colormaps) == 1 \
           or isinstance(colormaps, str):
            raise ValueError("A MultivarColormap must have more than one colormap.")
        colormaps = list(colormaps)  # ensure cmaps is a list, i.e. not a tuple
        for i, cmap in enumerate(colormaps):
            if isinstance(cmap, str):
                colormaps[i] = mpl.colormaps[cmap]
            elif not isinstance(cmap, Colormap):
                raise ValueError("colormaps must be a list of objects that subclass"
                                 " Colormap or a name found in the colormap registry.")

        self._colormaps = colormaps
        _api.check_in_list(['sRGB_add', 'sRGB_sub'], combination_mode=combination_mode)
        self._combination_mode = combination_mode
        self.n_variates = len(colormaps)
        self._rgba_bad = (0.0, 0.0, 0.0, 0.0)  # If bad, don't paint anything.
