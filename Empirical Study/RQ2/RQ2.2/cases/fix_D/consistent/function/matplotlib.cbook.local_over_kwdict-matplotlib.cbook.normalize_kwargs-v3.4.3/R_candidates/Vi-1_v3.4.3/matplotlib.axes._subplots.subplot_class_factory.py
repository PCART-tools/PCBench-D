@functools.lru_cache(None)
def subplot_class_factory(axes_class=None):
    """
    Make a new class that inherits from `.SubplotBase` and the
    given axes_class (which is assumed to be a subclass of `.axes.Axes`).
    This is perhaps a little bit roundabout to make a new class on
    the fly like this, but it means that a new Subplot class does
    not have to be created for every type of Axes.
    """
    if axes_class is None:
        _api.warn_deprecated(
            "3.3", message="Support for passing None to subplot_class_factory "
            "is deprecated since %(since)s; explicitly pass the default Axes "
            "class instead. This will become an error %(removal)s.")
        axes_class = Axes

    try:
        # Avoid creating two different instances of GeoAxesSubplot...
        # Only a temporary backcompat fix.  This should be removed in
        # 3.4
        return next(cls for cls in SubplotBase.__subclasses__()
                    if cls.__bases__ == (SubplotBase, axes_class))
    except StopIteration:
        # if we have already wrapped this class, declare victory!
        if issubclass(axes_class, SubplotBase):
            return axes_class

        return type("%sSubplot" % axes_class.__name__,
                    (SubplotBase, axes_class),
                    {'_axes_class': axes_class})
