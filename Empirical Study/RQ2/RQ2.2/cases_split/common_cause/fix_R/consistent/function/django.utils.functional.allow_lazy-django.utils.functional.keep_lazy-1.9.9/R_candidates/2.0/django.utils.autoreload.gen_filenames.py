def gen_filenames(only_new=False):
    """
    Return a list of filenames referenced in sys.modules and translation files.
    """
    # N.B. ``list(...)`` is needed, because this runs in parallel with
    # application code which might be mutating ``sys.modules``, and this will
    # fail with RuntimeError: cannot mutate dictionary while iterating
    global _cached_modules, _cached_filenames
    module_values = set(sys.modules.values())
    _cached_filenames = clean_files(_cached_filenames)
    if _cached_modules == module_values:
        # No changes in module list, short-circuit the function
        if only_new:
            return []
        else:
            return _cached_filenames + clean_files(_error_files)

    new_modules = module_values - _cached_modules
    new_filenames = clean_files(
        [filename.__file__ for filename in new_modules
         if hasattr(filename, '__file__')])

    if not _cached_filenames and settings.USE_I18N:
        # Add the names of the .mo files that can be generated
        # by compilemessages management command to the list of files watched.
        basedirs = [os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                 'conf', 'locale'),
                    'locale']
        for app_config in reversed(list(apps.get_app_configs())):
            basedirs.append(os.path.join(app_config.path, 'locale'))
        basedirs.extend(settings.LOCALE_PATHS)
        basedirs = [os.path.abspath(basedir) for basedir in basedirs
                    if os.path.isdir(basedir)]
        for basedir in basedirs:
            for dirpath, dirnames, locale_filenames in os.walk(basedir):
                for filename in locale_filenames:
                    if filename.endswith('.mo'):
                        new_filenames.append(os.path.join(dirpath, filename))

    _cached_modules = _cached_modules.union(new_modules)
    _cached_filenames += new_filenames
    if only_new:
        return new_filenames + clean_files(_error_files)
    else:
        return _cached_filenames + clean_files(_error_files)
