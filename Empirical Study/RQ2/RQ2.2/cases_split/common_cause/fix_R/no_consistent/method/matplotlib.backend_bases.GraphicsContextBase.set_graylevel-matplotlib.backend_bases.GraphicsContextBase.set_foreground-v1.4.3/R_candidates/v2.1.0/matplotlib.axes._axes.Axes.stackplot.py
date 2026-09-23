    @_preprocess_data(replace_all_args=True, label_namer=None)
    def stackplot(self, x, *args, **kwargs):
        return mstack.stackplot(self, x, *args, **kwargs)
