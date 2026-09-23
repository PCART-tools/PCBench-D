class OneToOneField(ForeignKey):
    """
    A OneToOneField is essentially the same as a ForeignKey, with the exception
    that it always carries a "unique" constraint with it and the reverse
    relation always returns the object pointed to (since there will only ever
    be one), rather than returning a list.
    """

    # Field flags
    many_to_many = False
    many_to_one = False
    one_to_many = False
    one_to_one = True

    related_accessor_class = ReverseOneToOneDescriptor
    rel_class = OneToOneRel

    description = _("One-to-one relationship")

    def __init__(self, to, on_delete=None, to_field=None, **kwargs):
        kwargs['unique'] = True

        if on_delete is None:
            warnings.warn(
                "on_delete will be a required arg for %s in Django 2.0. "
                "Set it to models.CASCADE if you want to maintain the current default behavior. "
                "See https://docs.djangoproject.com/en/%s/ref/models/fields/"
                "#django.db.models.ForeignKey.on_delete" % (
                    self.__class__.__name__,
                    get_docs_version(),
                ),
                RemovedInDjango20Warning, 2)
            on_delete = CASCADE

        elif not callable(on_delete):
            warnings.warn(
                "The signature for {0} will change in Django 2.0. "
                "Pass to_field='{1}' as a kwarg instead of as an arg.".format(
                    self.__class__.__name__,
                    on_delete,
                ),
                RemovedInDjango20Warning, 2)
            to_field = on_delete
            on_delete = CASCADE  # Avoid warning in superclass

        super(OneToOneField, self).__init__(to, on_delete, to_field=to_field, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(OneToOneField, self).deconstruct()
        if "unique" in kwargs:
            del kwargs['unique']
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        if self.remote_field.parent_link:
            return None
        return super(OneToOneField, self).formfield(**kwargs)

    def save_form_data(self, instance, data):
        if isinstance(data, self.remote_field.model):
            setattr(instance, self.name, data)
        else:
            setattr(instance, self.attname, data)

    def _check_unique(self, **kwargs):
        # Override ForeignKey since check isn't applicable here.
        return []
