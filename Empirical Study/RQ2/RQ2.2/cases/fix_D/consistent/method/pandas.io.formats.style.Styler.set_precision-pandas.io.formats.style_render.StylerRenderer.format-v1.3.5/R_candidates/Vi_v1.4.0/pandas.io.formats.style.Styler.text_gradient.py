    @doc(
        background_gradient,
        name="text",
        alt="background",
        image_prefix="tg",
        axis="{0 or 'index', 1 or 'columns', None}",
        text_threshold="This argument is ignored (only used in `background_gradient`).",
    )
    def text_gradient(
        self,
        cmap="PuBu",
        low: float = 0,
        high: float = 0,
        axis: Axis | None = 0,
        subset: Subset | None = None,
        vmin: float | None = None,
        vmax: float | None = None,
        gmap: Sequence | None = None,
    ) -> Styler:
        if subset is None and gmap is None:
            subset = self.data.select_dtypes(include=np.number).columns

        return self.apply(
            _background_gradient,
            cmap=cmap,
            subset=subset,
            axis=axis,
            low=low,
            high=high,
            vmin=vmin,
            vmax=vmax,
            gmap=gmap,
            text_only=True,
        )
