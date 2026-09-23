    @cached_property
    def RelatedObjectDoesNotExist(self):
        # The exception isn't created at initialization time for the sake of
        # consistency with `ForwardManyToOneDescriptor`.
        return type(
            str('RelatedObjectDoesNotExist'),
            (self.related.related_model.DoesNotExist, AttributeError),
            {}
        )
