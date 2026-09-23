    @Appender(_shared_docs['transpose'] % _shared_doc_kwargs)
    def transpose(self, *args, **kwargs):
        return super(Panel, self).transpose(*args, **kwargs)
