def watch_for_translation_changes(sender, **kwargs):
    """Register file watchers for .mo files in potential locale paths."""
    from django.conf import settings

    if settings.USE_I18N:
        directories = [Path('locale')]
        directories.extend(Path(config.path) / 'locale' for config in apps.get_app_configs())
        directories.extend(Path(p) for p in settings.LOCALE_PATHS)
        for path in directories:
            sender.watch_dir(path, '**/*.mo')
