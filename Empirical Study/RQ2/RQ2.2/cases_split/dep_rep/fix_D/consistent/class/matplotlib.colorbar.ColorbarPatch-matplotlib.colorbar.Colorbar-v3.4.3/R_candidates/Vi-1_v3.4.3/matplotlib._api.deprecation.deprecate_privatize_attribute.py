class deprecate_privatize_attribute:
    """
    Helper to deprecate public access to an attribute.

    This helper should only be used at class scope, as follows::

        class Foo:
            attr = _deprecate_privatize_attribute(*args, **kwargs)

    where *all* parameters are forwarded to `deprecated`.  This form makes
    ``attr`` a property which forwards access to ``self._attr`` (same name but
    with a leading underscore), with a deprecation warning.  Note that the
    attribute name is derived from *the name this helper is assigned to*.
    """

    def __init__(self, *args, **kwargs):
        self.deprecator = deprecated(*args, **kwargs)

    def __set_name__(self, owner, name):
        setattr(owner, name, self.deprecator(
            property(lambda self: getattr(self, f"_{name}")), name=name))
