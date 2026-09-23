    def _populate_validators(self, class_validators):
        if not self.sub_fields:
            get_validators = getattr(self.type_, 'get_validators', None)
            v_funcs = (
                *tuple(v.func for v in class_validators if not v.whole and v.pre),
                *(get_validators() if get_validators else find_validators(self.type_)),
                *tuple(v.func for v in class_validators if not v.whole and not v.pre),
            )
            self.validators = self._prep_vals(v_funcs)

        if class_validators:
            self.whole_pre_validators = self._prep_vals(v.func for v in class_validators if v.whole and v.pre)
            self.whole_post_validators = self._prep_vals(v.func for v in class_validators if v.whole and not v.pre)
