    def __init__(self, N=256, M=256, shape='square', origin=(0, 0),
                 name='bivariate colormap'):
        """
        Parameters
        ----------
        N : int, default: 256
            The number of RGB quantization levels along the first axis.
        M : int, default: 256
            The number of RGB quantization levels along the second axis.
        shape : {'square', 'circle', 'ignore', 'circleignore'}

            - 'square' each variate is clipped to [0,1] independently
            - 'circle' the variates are clipped radially to the center
              of the colormap, and a circular mask is applied when the colormap
              is displayed
            - 'ignore' the variates are not clipped, but instead assigned the
              'outside' color
            - 'circleignore' a circular mask is applied, but the data is not
              clipped and instead assigned the 'outside' color

        origin : (float, float), default: (0,0)
            The relative origin of the colormap. Typically (0, 0), for colormaps
            that are linear on both axis, and (.5, .5) for circular colormaps.
            Used when getting 1D colormaps from 2D colormaps.
        name : str, optional
            The name of the colormap.
        """

        self.name = name
        self.N = int(N)  # ensure that N is always int
        self.M = int(M)
        _api.check_in_list(['square', 'circle', 'ignore', 'circleignore'], shape=shape)
        self._shape = shape
        self._rgba_bad = (0.0, 0.0, 0.0, 0.0)  # If bad, don't paint anything.
        self._rgba_outside = (1.0, 0.0, 1.0, 1.0)
        self._isinit = False
        self.n_variates = 2
        self._origin = (float(origin[0]), float(origin[1]))
        '''#: When this colormap exists on a scalar mappable and colorbar_extend
        #: is not False, colorbar creation will pick up ``colorbar_extend`` as
        #: the default value for the ``extend`` keyword in the
        #: `matplotlib.colorbar.Colorbar` constructor.
        self.colorbar_extend = False'''
