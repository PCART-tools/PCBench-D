    def __init__(self, to, on_delete=None, related_name=None, related_query_name=None,
                 limit_choices_to=None, parent_link=False, to_field=None,
                 db_constraint=True, **kwargs):
        try:
            to._meta.model_name
        except AttributeError:
            assert isinstance(to, six.string_types), (
                "%s(%r) is invalid. First parameter to ForeignKey must be "
                "either a model, a model name, or the string %r" % (
                    self.__class__.__name__, to,
                    RECURSIVE_RELATIONSHIP_CONSTANT,
                )
            )
        else:
            # For backwards compatibility purposes, we need to *try* and set
            # the to_field during FK construction. It won't be guaranteed to
            # be correct until contribute_to_class is called. Refs #12190.
            to_field = to_field or (to._meta.pk and to._meta.pk.name)

        if on_delete is None:
            warnings.warn(
                "on_delete will be a required arg for %s in Django 2.0. Set "
                "it to models.CASCADE on models and in existing migrations "
                "if you want to maintain the current default behavior. "
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
            on_delete, to_field = to_field, on_delete

        kwargs['rel'] = self.rel_class(
            self, to, to_field,
            related_name=related_name,
            related_query_name=related_query_name,
            limit_choices_to=limit_choices_to,
            parent_link=parent_link,
            on_delete=on_delete,
        )

        kwargs['db_index'] = kwargs.get('db_index', True)

        super(ForeignKey, self).__init__(
            to, on_delete, from_fields=['self'], to_fields=[to_field], **kwargs)

        self.db_constraint = db_constraint
