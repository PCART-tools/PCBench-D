def default_opener(filename):
    """Opens `filename` using system's default program.

    .. deprecated:: 2.6
       default_opener is deprecated and will be removed in version 3.0.
       Consider an image processing library to open images, such as Pillow::

           from PIL import Image
           Image.open(filename).show()

    Parameters
    ----------
    filename : str
        The path of the file to be opened.

    """
    warnings.warn(
        "default_opener is deprecated and will be removed in version 3.0. ",
        DeprecationWarning,
    )
    from subprocess import call

    cmds = {
        "darwin": ["open"],
        "linux": ["xdg-open"],
        "linux2": ["xdg-open"],
        "win32": ["cmd.exe", "/C", "start", ""],
    }
    cmd = cmds[sys.platform] + [filename]
    call(cmd)
