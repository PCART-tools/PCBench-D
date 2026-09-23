    @warn_about_renamed_method(
        'Field', '_get_val_from_obj', 'value_from_object',
        RemovedInDjango20Warning
    )
    def _get_val_from_obj(self, obj):
        if obj is not None:
            return getattr(obj, self.attname)
        else:
            return self.get_default()
