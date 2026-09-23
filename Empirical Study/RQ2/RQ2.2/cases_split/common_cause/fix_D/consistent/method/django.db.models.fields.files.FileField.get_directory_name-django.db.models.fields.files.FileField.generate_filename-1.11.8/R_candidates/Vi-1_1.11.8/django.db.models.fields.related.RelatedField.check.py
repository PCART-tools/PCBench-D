    def check(self, **kwargs):
        errors = super(RelatedField, self).check(**kwargs)
        errors.extend(self._check_related_name_is_valid())
        errors.extend(self._check_related_query_name_is_valid())
        errors.extend(self._check_relation_model_exists())
        errors.extend(self._check_referencing_to_swapped_model())
        errors.extend(self._check_clashes())
        return errors
