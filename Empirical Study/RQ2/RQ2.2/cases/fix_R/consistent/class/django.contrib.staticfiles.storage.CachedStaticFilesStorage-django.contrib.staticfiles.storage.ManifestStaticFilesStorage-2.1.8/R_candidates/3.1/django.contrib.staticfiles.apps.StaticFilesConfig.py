class StaticFilesConfig(AppConfig):
    name = 'django.contrib.staticfiles'
    verbose_name = _("Static Files")
    ignore_patterns = ['CVS', '.*', '*~']

    def ready(self):
        checks.register(check_finders, checks.Tags.staticfiles)
