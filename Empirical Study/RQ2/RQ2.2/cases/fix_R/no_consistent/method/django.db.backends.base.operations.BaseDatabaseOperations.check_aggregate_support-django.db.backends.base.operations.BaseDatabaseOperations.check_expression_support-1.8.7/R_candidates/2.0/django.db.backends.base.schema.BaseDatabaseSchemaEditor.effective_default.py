    def effective_default(self, field):
        """Return a field's effective database default value."""
        if field.has_default():
            default = field.get_default()
        elif not field.null and field.blank and field.empty_strings_allowed:
            if field.get_internal_type() == "BinaryField":
                default = bytes()
            else:
                default = str()
        elif getattr(field, 'auto_now', False) or getattr(field, 'auto_now_add', False):
            default = datetime.now()
            internal_type = field.get_internal_type()
            if internal_type == 'DateField':
                default = default.date
            elif internal_type == 'TimeField':
                default = default.time
            elif internal_type == 'DateTimeField':
                default = timezone.now
        else:
            default = None
        # If it's a callable, call it
        if callable(default):
            default = default()
        # Run it through the field's get_db_prep_save method so we can send it
        # to the database.
        default = field.get_db_prep_save(default, self.connection)
        return default
