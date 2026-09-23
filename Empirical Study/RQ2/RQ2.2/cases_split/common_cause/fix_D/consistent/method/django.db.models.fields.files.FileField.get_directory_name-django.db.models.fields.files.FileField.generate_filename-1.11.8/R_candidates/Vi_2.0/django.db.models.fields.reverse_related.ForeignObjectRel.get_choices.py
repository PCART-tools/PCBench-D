    def get_choices(self, include_blank=True, blank_choice=BLANK_CHOICE_DASH):
        """
        Return choices with a default blank choices included, for use
        as <select> choices for this field.

        Analog of django.db.models.fields.Field.get_choices(), provided
        initially for utilization by RelatedFieldListFilter.
        """
        return (blank_choice if include_blank else []) + [
            (x.pk, str(x)) for x in self.related_model._default_manager.all()
        ]
