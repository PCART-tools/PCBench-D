    def _check_choices(self):
        if self.choices:
            if (isinstance(self.choices, six.string_types) or
                    not is_iterable(self.choices)):
                return [
                    checks.Error(
                        "'choices' must be an iterable (e.g., a list or tuple).",
                        obj=self,
                        id='fields.E004',
                    )
                ]
            elif any(isinstance(choice, six.string_types) or
                     not is_iterable(choice) or len(choice) != 2
                     for choice in self.choices):
                return [
                    checks.Error(
                        "'choices' must be an iterable containing "
                        "(actual value, human readable name) tuples.",
                        obj=self,
                        id='fields.E005',
                    )
                ]
            else:
                return []
        else:
            return []
