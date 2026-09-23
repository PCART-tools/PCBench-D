def _win32RegistryFonts(reg_domain, base_dir):
    r"""
    Search for fonts in the Windows registry.

    Parameters
    ----------
    reg_domain : int
        The top level registry domain (e.g. HKEY_LOCAL_MACHINE).

    base_dir : str
        The path to the folder where the font files are usually located (e.g.
        C:\Windows\Fonts). If only the filename of the font is stored in the
        registry, the absolute path is built relative to this base directory.

    Returns
    -------
    `set`
        `pathlib.Path` objects with the absolute path to the font files found.

    """
    import winreg
    items = set()

    for reg_path in MSFontDirectories:
        try:
            with winreg.OpenKey(reg_domain, reg_path) as local:
                for j in range(winreg.QueryInfoKey(local)[1]):
                    # value may contain the filename of the font or its
                    # absolute path.
                    key, value, tp = winreg.EnumValue(local, j)
                    if not isinstance(value, str):
                        continue
                    try:
                        # If value contains already an absolute path, then it
                        # is not changed further.
                        path = Path(base_dir, value).resolve()
                    except RuntimeError:
                        # Don't fail with invalid entries.
                        continue

                    items.add(path)
        except (OSError, MemoryError):
            continue

    return items
