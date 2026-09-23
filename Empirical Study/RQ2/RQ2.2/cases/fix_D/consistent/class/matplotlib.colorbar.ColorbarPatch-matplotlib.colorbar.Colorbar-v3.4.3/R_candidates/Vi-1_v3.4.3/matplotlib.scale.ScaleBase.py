class ScaleBase:
    """
    The base class for all scales.

    Scales are separable transformations, working on a single dimension.

    Any subclasses will want to override:

    - :attr:`name`
    - :meth:`get_transform`
    - :meth:`set_default_locators_and_formatters`

    And optionally:

    - :meth:`limit_range_for_scale`

    """

    def __init__(self, axis):
        r"""
        Construct a new scale.

        Notes
        -----
        The following note is for scale implementors.

        For back-compatibility reasons, scales take an `~matplotlib.axis.Axis`
        object as first argument.  However, this argument should not
        be used: a single scale object should be usable by multiple
        `~matplotlib.axis.Axis`\es at the same time.
        """

    def get_transform(self):
        """
        Return the :class:`~matplotlib.transforms.Transform` object
        associated with this scale.
        """
        raise NotImplementedError()

    def set_default_locators_and_formatters(self, axis):
        """
        Set the locators and formatters of *axis* to instances suitable for
        this scale.
        """
        raise NotImplementedError()

    def limit_range_for_scale(self, vmin, vmax, minpos):
        """
        Return the range *vmin*, *vmax*, restricted to the
        domain supported by this scale (if any).

        *minpos* should be the minimum positive value in the data.
        This is used by log scales to determine a minimum value.
        """
        return vmin, vmax
