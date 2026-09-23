    def _deprecate_noninstance(self, _name, _types, **kwargs):
        """
        For each *key, value* pair in *kwargs*, check that *value* is an
        instance of one of *_types*; if not, raise an appropriate deprecation.
        """
        for key, value in kwargs.items():
            if not isinstance(value, _types):
                _api.warn_deprecated(
                    '3.5', name=_name,
                    message=f'Passing argument *{key}* of unexpected type '
                    f'{type(value).__qualname__} to %(name)s which only '
                    f'accepts {_types} is deprecated since %(since)s and will '
                    'become an error %(removal)s.')
