    def __init__(self, to, on_delete=None, to_field=None, **kwargs):
        kwargs['unique'] = True

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
            to_field = on_delete
            on_delete = CASCADE  # Avoid warning in superclass

        super(OneToOneField, self).__init__(to, on_delete, to_field=to_field, **kwargs)
