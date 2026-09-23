def out_of_date(original, derived):
    """
    Return whether *derived* is out-of-date relative to *original*, both of
    which are full file paths.
    """
    return (not os.path.exists(derived) or
            (os.path.exists(original) and
             os.stat(derived).st_mtime < os.stat(original).st_mtime))
