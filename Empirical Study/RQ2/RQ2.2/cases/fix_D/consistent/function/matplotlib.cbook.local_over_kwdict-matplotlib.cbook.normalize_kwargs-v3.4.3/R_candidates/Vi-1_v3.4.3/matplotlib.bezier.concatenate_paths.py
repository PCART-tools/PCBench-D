@_api.deprecated("3.3", alternative="Path.make_compound_path()")
def concatenate_paths(paths):
    """Concatenate a list of paths into a single path."""
    from .path import Path
    return Path.make_compound_path(*paths)
