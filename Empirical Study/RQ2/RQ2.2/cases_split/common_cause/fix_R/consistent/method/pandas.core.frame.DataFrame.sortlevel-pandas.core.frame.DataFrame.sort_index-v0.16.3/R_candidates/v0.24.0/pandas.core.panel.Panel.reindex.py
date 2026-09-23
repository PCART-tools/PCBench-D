    @Substitution(**_shared_doc_kwargs)
    @Appender(NDFrame.reindex.__doc__)
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

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", FutureWarning)
            # do not warn about constructing Panel when reindexing
            result = super(Panel, self).reindex(**kwargs)
        return result
