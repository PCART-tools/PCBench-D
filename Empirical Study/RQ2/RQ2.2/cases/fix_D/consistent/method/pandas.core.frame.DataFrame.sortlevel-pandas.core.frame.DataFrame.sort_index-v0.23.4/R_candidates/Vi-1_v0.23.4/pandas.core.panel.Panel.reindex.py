    @Appender(_shared_docs['reindex'] % _shared_doc_kwargs)
    def reindex(self, *args, **kwargs):
        major = kwargs.pop("major", None)
        minor = kwargs.pop('minor', None)

        if major is not None:
            if kwargs.get("major_axis"):
                raise TypeError("Cannot specify both 'major' and 'major_axis'")
            kwargs['major_axis'] = major
        if minor is not None:
            if kwargs.get("minor_axis"):
                raise TypeError("Cannot specify both 'minor' and 'minor_axis'")

            kwargs['minor_axis'] = minor
        axes = validate_axis_style_args(self, args, kwargs, 'labels',
                                        'reindex')
        kwargs.update(axes)
        kwargs.pop('axis', None)
        kwargs.pop('labels', None)
        return super(Panel, self).reindex(**kwargs)
