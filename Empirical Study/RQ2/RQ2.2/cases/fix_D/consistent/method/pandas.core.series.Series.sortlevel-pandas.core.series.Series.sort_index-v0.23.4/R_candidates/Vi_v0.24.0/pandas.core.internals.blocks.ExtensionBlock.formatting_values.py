    def formatting_values(self):
        # Deprecating the ability to override _formatting_values.
        # Do the warning here, it's only user in pandas, since we
        # have to check if the subclass overrode it.
        fv = getattr(type(self.values), '_formatting_values', None)
        if fv and fv != ExtensionArray._formatting_values:
            msg = (
                "'ExtensionArray._formatting_values' is deprecated. "
                "Specify 'ExtensionArray._formatter' instead."
            )
            warnings.warn(msg, DeprecationWarning, stacklevel=10)
            return self.values._formatting_values()

        return self.values
