    @_api.make_keyword_only("3.6", name="zoom")
    def __init__(self, arr,
                 zoom=1,
                 cmap=None,
                 norm=None,
                 interpolation=None,
                 origin=None,
                 filternorm=True,
                 filterrad=4.0,
                 resample=False,
                 dpi_cor=True,
                 **kwargs
                 ):

        super().__init__()
        self._dpi_cor = dpi_cor

        self.image = BboxImage(bbox=self.get_window_extent,
                               cmap=cmap,
                               norm=norm,
                               interpolation=interpolation,
                               origin=origin,
                               filternorm=filternorm,
                               filterrad=filterrad,
                               resample=resample,
                               **kwargs
                               )

        self._children = [self.image]

        self.set_zoom(zoom)
        self.set_data(arr)
