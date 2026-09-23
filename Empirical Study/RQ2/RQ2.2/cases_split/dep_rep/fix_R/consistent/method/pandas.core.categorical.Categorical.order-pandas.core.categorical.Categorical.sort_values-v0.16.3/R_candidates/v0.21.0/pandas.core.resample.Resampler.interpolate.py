    @Appender(_shared_docs['interpolate'] % _shared_docs_kwargs)
    def interpolate(self, method='linear', axis=0, limit=None, inplace=False,
                    limit_direction='forward', downcast=None, **kwargs):
        """
        Interpolate values according to different methods.

        .. versionadded:: 0.18.1
        """
        result = self._upsample(None)
        return result.interpolate(method=method, axis=axis, limit=limit,
                                  inplace=inplace,
                                  limit_direction=limit_direction,
                                  downcast=downcast, **kwargs)
