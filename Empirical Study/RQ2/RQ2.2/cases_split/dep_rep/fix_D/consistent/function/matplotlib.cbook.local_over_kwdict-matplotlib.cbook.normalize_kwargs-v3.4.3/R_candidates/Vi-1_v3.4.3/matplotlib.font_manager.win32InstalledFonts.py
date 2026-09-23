def win32InstalledFonts(directory=None, fontext='ttf'):
    """
    Search for fonts in the specified font directory, or use the
    system directories if none given. Additionally, it is searched for user
    fonts installed. A list of TrueType font filenames are returned by default,
    or AFM fonts if *fontext* == 'afm'.
    """
    import winreg

    if directory is None:
        directory = win32FontDirectory()

    fontext = ['.' + ext for ext in get_fontext_synonyms(fontext)]

    items = set()

    # System fonts
    items.update(_win32RegistryFonts(winreg.HKEY_LOCAL_MACHINE, directory))

    # User fonts
    for userdir in MSUserFontDirectories:
        items.update(_win32RegistryFonts(winreg.HKEY_CURRENT_USER, userdir))

    # Keep only paths with matching file extension.
    return [str(path) for path in items if path.suffix.lower() in fontext]
