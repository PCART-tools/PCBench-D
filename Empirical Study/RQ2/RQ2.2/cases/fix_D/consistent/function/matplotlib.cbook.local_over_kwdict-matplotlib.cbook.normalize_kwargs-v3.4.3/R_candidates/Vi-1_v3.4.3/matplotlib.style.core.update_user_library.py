def update_user_library(library):
    """Update style library with user-defined rc files."""
    for stylelib_path in iter_user_libraries():
        styles = read_style_directory(stylelib_path)
        update_nested_dict(library, styles)
    return library
