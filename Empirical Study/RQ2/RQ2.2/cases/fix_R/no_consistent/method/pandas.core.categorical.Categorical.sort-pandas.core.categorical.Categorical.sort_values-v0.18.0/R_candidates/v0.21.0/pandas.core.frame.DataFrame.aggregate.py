    @Appender(_agg_doc)
    @Appender(_shared_docs['aggregate'] % dict(
        versionadded='.. versionadded:: 0.20.0',
        **_shared_doc_kwargs))
    def aggregate(self, func, axis=0, *args, **kwargs):
        axis = self._get_axis_number(axis)

        # TODO: flipped axis
        result = None
        if axis == 0:
            try:
                result, how = self._aggregate(func, axis=0, *args, **kwargs)
            except TypeError:
                pass
        if result is None:
            return self.apply(func, axis=axis, args=args, **kwargs)
        return result
