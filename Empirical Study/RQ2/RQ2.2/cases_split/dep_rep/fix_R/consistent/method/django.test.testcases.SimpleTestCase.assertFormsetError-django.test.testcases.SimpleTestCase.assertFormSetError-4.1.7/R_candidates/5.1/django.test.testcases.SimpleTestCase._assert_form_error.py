    def _assert_form_error(self, form, field, errors, msg_prefix, form_repr):
        if not form.is_bound:
            self.fail(
                f"{msg_prefix}The {form_repr} is not bound, it will never have any "
                f"errors."
            )

        if field is not None and field not in form.fields:
            self.fail(
                f"{msg_prefix}The {form_repr} does not contain the field {field!r}."
            )
        if field is None:
            field_errors = form.non_field_errors()
            failure_message = f"The non-field errors of {form_repr} don't match."
        else:
            field_errors = form.errors.get(field, [])
            failure_message = (
                f"The errors of field {field!r} on {form_repr} don't match."
            )

        self.assertEqual(field_errors, errors, msg_prefix + failure_message)
