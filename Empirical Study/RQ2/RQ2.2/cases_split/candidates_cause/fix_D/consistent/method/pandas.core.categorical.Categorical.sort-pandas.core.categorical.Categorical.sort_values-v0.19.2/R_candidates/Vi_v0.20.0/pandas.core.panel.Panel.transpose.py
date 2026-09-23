    @Appender(_shared_docs['transpose'] % _shared_doc_kwargs)
    def transpose(self, *args, **kwargs):
        # check if a list of axes was passed in instead as a
        # single *args element
        if (len(args) == 1 and hasattr(args[0], '__iter__') and
                not is_string_like(args[0])):
            axes = args[0]
        else:
            axes = args

        if 'axes' in kwargs and axes:
            raise TypeError("transpose() got multiple values for "
                            "keyword argument 'axes'")
        elif not axes:
            axes = kwargs.pop('axes', ())

        return super(Panel, self).transpose(*axes, **kwargs)
