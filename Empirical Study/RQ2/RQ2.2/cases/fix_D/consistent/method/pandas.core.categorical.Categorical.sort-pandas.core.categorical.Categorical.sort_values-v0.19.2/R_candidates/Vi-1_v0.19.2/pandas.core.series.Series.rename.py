    @Appender(generic._shared_docs['rename'] % _shared_doc_kwargs)
    def rename(self, index=None, **kwargs):
        non_mapping = is_scalar(index) or (is_list_like(index) and
                                           not is_dict_like(index))
        if non_mapping:
            return self._set_name(index, inplace=kwargs.get('inplace'))
        return super(Series, self).rename(index=index, **kwargs)
