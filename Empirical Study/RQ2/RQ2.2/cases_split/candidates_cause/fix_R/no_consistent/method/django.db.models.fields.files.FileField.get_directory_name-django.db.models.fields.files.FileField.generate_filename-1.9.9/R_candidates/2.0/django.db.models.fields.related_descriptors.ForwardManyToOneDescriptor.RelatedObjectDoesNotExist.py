    @cached_property
    def RelatedObjectDoesNotExist(self):
        # The exception can't be created at initialization time since the
        # related model might not be resolved yet; `self.field.model` might
        # still be a string model reference.
        return type(
            'RelatedObjectDoesNotExist',
            (self.field.remote_field.model.DoesNotExist, AttributeError),
            {}
        )
