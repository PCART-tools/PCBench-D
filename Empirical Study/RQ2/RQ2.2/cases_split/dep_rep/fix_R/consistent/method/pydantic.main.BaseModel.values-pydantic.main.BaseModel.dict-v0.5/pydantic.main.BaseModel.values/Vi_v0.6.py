    def values(self, **kwargs):
        warnings.warn('.values(...) is depreciated and will be removed in future, '
                      'it has been replaced by .dict(...)', DeprecationWarning)
        return self.dict(**kwargs)
