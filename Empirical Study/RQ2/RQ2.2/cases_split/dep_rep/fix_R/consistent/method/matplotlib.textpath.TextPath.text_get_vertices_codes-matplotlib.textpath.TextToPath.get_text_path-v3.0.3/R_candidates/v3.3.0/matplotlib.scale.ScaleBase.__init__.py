    def __init__(self, axis, **kwargs):
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
        if kwargs:
            warn_deprecated(
                '3.2', removal='3.4',
                message=(
                    f"ScaleBase got an unexpected keyword argument "
                    f"{next(iter(kwargs))!r}. This will become an error "
                    "%(removal)s.")
            )
