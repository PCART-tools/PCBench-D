    def __getitem__(self, key):
        if key in _DEPRECATED_SEABORN_STYLES:
            _api.warn_deprecated("3.6", message=_DEPRECATED_SEABORN_MSG)
            key = _DEPRECATED_SEABORN_STYLES[key]

        return dict.__getitem__(self, key)
