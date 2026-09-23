    def __init_subclass__(cls, **kwargs):
        parent_uses_cla = super(cls, cls)._subclass_uses_cla
        if 'cla' in cls.__dict__:
            _api.warn_deprecated(
                '3.6',
                pending=True,
                message=f'Overriding `Axes.cla` in {cls.__qualname__} is '
                'pending deprecation in %(since)s and will be fully '
                'deprecated in favor of `Axes.clear` in the future. '
                'Please report '
                f'this to the {cls.__module__!r} author.')
        cls._subclass_uses_cla = 'cla' in cls.__dict__ or parent_uses_cla
        super().__init_subclass__(**kwargs)
