    def get_choices(self, include_blank=True, blank_choice=BLANK_CHOICE_DASH, limit_choices_to=None):
        """
        Return choices with a default blank choices included, for use
        as <select> choices for this field.
        """
        blank_defined = False
        choices = list(self.choices) if self.choices else []
        named_groups = choices and isinstance(choices[0][1], (list, tuple))
        if not named_groups:
            for choice, __ in choices:
                if choice in ('', None):
                    blank_defined = True
                    break

        first_choice = (blank_choice if include_blank and
                        not blank_defined else [])
        if self.choices:
            return first_choice + choices
        rel_model = self.remote_field.model
        limit_choices_to = limit_choices_to or self.get_limit_choices_to()
        if hasattr(self.remote_field, 'get_related_field'):
            lst = [(getattr(x, self.remote_field.get_related_field().attname),
                   smart_text(x))
                   for x in rel_model._default_manager.complex_filter(
                       limit_choices_to)]
        else:
            lst = [(x.pk, smart_text(x))
                   for x in rel_model._default_manager.complex_filter(
                       limit_choices_to)]
        return first_choice + lst
