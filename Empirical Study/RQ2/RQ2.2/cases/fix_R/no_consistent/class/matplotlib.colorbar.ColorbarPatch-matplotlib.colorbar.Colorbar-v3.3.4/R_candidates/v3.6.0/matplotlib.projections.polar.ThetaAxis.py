class ThetaAxis(maxis.XAxis):
    """
    A theta Axis.

    This overrides certain properties of an `.XAxis` to provide special-casing
    for an angular axis.
    """
    __name__ = 'thetaaxis'
    axis_name = 'theta'  #: Read-only name identifying the axis.
    _tick_class = ThetaTick

    def _wrap_locator_formatter(self):
        self.set_major_locator(ThetaLocator(self.get_major_locator()))
        self.set_major_formatter(ThetaFormatter())
        self.isDefault_majloc = True
        self.isDefault_majfmt = True

    def clear(self):
        # docstring inherited
        super().clear()
        self.set_ticks_position('none')
        self._wrap_locator_formatter()

    def _set_scale(self, value, **kwargs):
        if value != 'linear':
            raise NotImplementedError(
                "The xscale cannot be set on a polar plot")
        super()._set_scale(value, **kwargs)
        # LinearScale.set_default_locators_and_formatters just set the major
        # locator to be an AutoLocator, so we customize it here to have ticks
        # at sensible degree multiples.
        self.get_major_locator().set_params(steps=[1, 1.5, 3, 4.5, 9, 10])
        self._wrap_locator_formatter()

    def _copy_tick_props(self, src, dest):
        """Copy the props from src tick to dest tick."""
        if src is None or dest is None:
            return
        super()._copy_tick_props(src, dest)

        # Ensure that tick transforms are independent so that padding works.
        trans = dest._get_text1_transform()[0]
        dest.label1.set_transform(trans + dest._text1_translate)
        trans = dest._get_text2_transform()[0]
        dest.label2.set_transform(trans + dest._text2_translate)
