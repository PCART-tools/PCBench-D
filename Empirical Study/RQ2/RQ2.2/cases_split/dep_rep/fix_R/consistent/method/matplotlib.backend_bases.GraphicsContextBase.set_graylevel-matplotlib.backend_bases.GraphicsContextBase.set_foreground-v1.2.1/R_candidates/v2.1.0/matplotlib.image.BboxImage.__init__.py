    def __init__(self, bbox,
                 cmap=None,
                 norm=None,
                 interpolation=None,
                 origin=None,
                 filternorm=1,
                 filterrad=4.0,
                 resample=False,
                 interp_at_native=True,
                 **kwargs
                 ):
        """
        cmap is a colors.Colormap instance
        norm is a colors.Normalize instance to map luminance to 0-1

        interp_at_native is a flag that determines whether or not
        interpolation should still be applied when the image is
        displayed at its native resolution.  A common use case for this
        is when displaying an image for annotational purposes; it is
        treated similarly to Photoshop (interpolation is only used when
        displaying the image at non-native resolutions).


        kwargs are an optional list of Artist keyword args

        """
        super(BboxImage, self).__init__(
            None,
            cmap=cmap,
            norm=norm,
            interpolation=interpolation,
            origin=origin,
            filternorm=filternorm,
            filterrad=filterrad,
            resample=resample,
            **kwargs
        )

        self.bbox = bbox
        self.interp_at_native = interp_at_native
        self._transform = IdentityTransform()
