    @Appender(_shared_docs['reindex'] % _shared_doc_kwargs)
    def reindex(self, items=None, major_axis=None, minor_axis=None, **kwargs):
        major_axis = (major_axis if major_axis is not None
                      else kwargs.pop('major', None))
        minor_axis = (minor_axis if minor_axis is not None
                      else kwargs.pop('minor', None))
        return super(Panel, self).reindex(items=items, major_axis=major_axis,
                                          minor_axis=minor_axis, **kwargs)
