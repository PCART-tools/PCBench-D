    def contribute_to_class(self, cls, name, private_only=False, virtual_only=NOT_PROVIDED):
        """
        Register the field with the model class it belongs to.

        If private_only is True, a separate instance of this field will be
        created for every subclass of cls, even if cls is not an abstract
        model.
        """
        if virtual_only is not NOT_PROVIDED:
            warnings.warn(
                "The `virtual_only` argument of Field.contribute_to_class() "
                "has been renamed to `private_only`.",
                RemovedInDjango20Warning, stacklevel=2
            )
            private_only = virtual_only
        self.set_attributes_from_name(name)
        self.model = cls
        if private_only:
            cls._meta.add_field(self, private=True)
        else:
            cls._meta.add_field(self)
        if self.column:
            # Don't override classmethods with the descriptor. This means that
            # if you have a classmethod and a field with the same name, then
            # such fields can't be deferred (we don't have a check for this).
            if not getattr(cls, self.attname, None):
                setattr(cls, self.attname, DeferredAttribute(self.attname, cls))
        if self.choices:
            setattr(cls, 'get_%s_display' % self.name,
                    curry(cls._get_FIELD_display, field=self))
