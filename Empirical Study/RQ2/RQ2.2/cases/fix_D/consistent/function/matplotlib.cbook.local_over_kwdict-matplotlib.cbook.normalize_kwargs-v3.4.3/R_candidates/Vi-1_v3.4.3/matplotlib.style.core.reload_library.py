def reload_library():
    """Reload the style library."""
    global library
    library = update_user_library(_base_library)
    available[:] = sorted(library.keys())
