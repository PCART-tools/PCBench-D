@docstring.Substitution(
    "\n".join(map("- {}".format, sorted(rcsetup._validators, key=str.lower)))
)
class RcParams(MutableMapping, dict):
    """
    A dictionary object including validation.

    Validating functions are defined and associated with rc parameters in
    :mod:`matplotlib.rcsetup`.

    The list of rcParams is:

    %s

    See Also
    --------
    :ref:`customizing-with-matplotlibrc-files`
    """

    validate = rcsetup._validators

    # validate values on the way in
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def __setitem__(self, key, val):
        try:
            if key in _deprecated_map:
                version, alt_key, alt_val, inverse_alt = _deprecated_map[key]
                _api.warn_deprecated(
                    version, name=key, obj_type="rcparam", alternative=alt_key)
                key = alt_key
                val = alt_val(val)
            elif key in _deprecated_remain_as_none and val is not None:
                version, = _deprecated_remain_as_none[key]
                _api.warn_deprecated(version, name=key, obj_type="rcparam")
            elif key in _deprecated_ignore_map:
                version, alt_key = _deprecated_ignore_map[key]
                _api.warn_deprecated(
                    version, name=key, obj_type="rcparam", alternative=alt_key)
                return
            elif key == 'backend':
                if val is rcsetup._auto_backend_sentinel:
                    if 'backend' in self:
                        return
            try:
                cval = self.validate[key](val)
            except ValueError as ve:
                raise ValueError(f"Key {key}: {ve}") from None
            dict.__setitem__(self, key, cval)
        except KeyError as err:
            raise KeyError(
                f"{key} is not a valid rc parameter (see rcParams.keys() for "
                f"a list of valid parameters)") from err

    def __getitem__(self, key):
        if key in _deprecated_map:
            version, alt_key, alt_val, inverse_alt = _deprecated_map[key]
            _api.warn_deprecated(
                version, name=key, obj_type="rcparam", alternative=alt_key)
            return inverse_alt(dict.__getitem__(self, alt_key))

        elif key in _deprecated_ignore_map:
            version, alt_key = _deprecated_ignore_map[key]
            _api.warn_deprecated(
                version, name=key, obj_type="rcparam", alternative=alt_key)
            return dict.__getitem__(self, alt_key) if alt_key else None

        # In theory, this should only ever be used after the global rcParams
        # has been set up, but better be safe e.g. in presence of breakpoints.
        elif key == "backend" and self is globals().get("rcParams"):
            val = dict.__getitem__(self, key)
            if val is rcsetup._auto_backend_sentinel:
                from matplotlib import pyplot as plt
                plt.switch_backend(rcsetup._auto_backend_sentinel)

        return dict.__getitem__(self, key)

    def __repr__(self):
        class_name = self.__class__.__name__
        indent = len(class_name) + 1
        with _api.suppress_matplotlib_deprecation_warning():
            repr_split = pprint.pformat(dict(self), indent=1,
                                        width=80 - indent).split('\n')
        repr_indented = ('\n' + ' ' * indent).join(repr_split)
        return '{}({})'.format(class_name, repr_indented)

    def __str__(self):
        return '\n'.join(map('{0[0]}: {0[1]}'.format, sorted(self.items())))

    def __iter__(self):
        """Yield sorted list of keys."""
        with _api.suppress_matplotlib_deprecation_warning():
            yield from sorted(dict.__iter__(self))

    def __len__(self):
        return dict.__len__(self)

    def find_all(self, pattern):
        """
        Return the subset of this RcParams dictionary whose keys match,
        using :func:`re.search`, the given ``pattern``.

        .. note::

            Changes to the returned dictionary are *not* propagated to
            the parent RcParams dictionary.

        """
        pattern_re = re.compile(pattern)
        return RcParams((key, value)
                        for key, value in self.items()
                        if pattern_re.search(key))

    def copy(self):
        return {k: dict.__getitem__(self, k) for k in self}
