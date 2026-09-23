    def get_prep_lookup(self):
        if not isinstance(self.lhs, MultiColSource) and self.rhs_is_direct_value():
            # If we get here, we are dealing with single-column relations.
            self.rhs = get_normalized_value(self.rhs, self.lhs)[0]
            # We need to run the related field's get_prep_value(). Consider case
            # ForeignKey to IntegerField given value 'abc'. The ForeignKey itself
            # doesn't have validation for non-integers, so we must run validation
            # using the target field.
            if self.prepare_rhs and hasattr(self.lhs.output_field, 'get_path_info'):
                # Get the target field. We can safely assume there is only one
                # as we don't get to the direct value branch otherwise.
                target_field = self.lhs.output_field.get_path_info()[-1].target_fields[-1]
                self.rhs = target_field.get_prep_value(self.rhs)

        return super(RelatedLookupMixin, self).get_prep_lookup()
