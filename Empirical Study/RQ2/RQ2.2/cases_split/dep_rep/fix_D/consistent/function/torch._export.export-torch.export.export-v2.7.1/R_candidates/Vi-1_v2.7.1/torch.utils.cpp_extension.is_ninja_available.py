def is_ninja_available():
    """Return ``True`` if the `ninja <https://ninja-build.org/>`_ build system is available on the system, ``False`` otherwise."""
    try:
        subprocess.check_output('ninja --version'.split())
    except Exception:
        return False
    else:
        return True
