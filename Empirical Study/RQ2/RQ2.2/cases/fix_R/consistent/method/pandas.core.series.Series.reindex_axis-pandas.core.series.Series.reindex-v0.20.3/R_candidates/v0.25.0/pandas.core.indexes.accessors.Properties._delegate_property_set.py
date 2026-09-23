    def _delegate_property_set(self, name, value, *args, **kwargs):
        raise ValueError(
            "modifications to a property of a datetimelike "
            "object are not supported. Change values on the "
            "original."
        )
