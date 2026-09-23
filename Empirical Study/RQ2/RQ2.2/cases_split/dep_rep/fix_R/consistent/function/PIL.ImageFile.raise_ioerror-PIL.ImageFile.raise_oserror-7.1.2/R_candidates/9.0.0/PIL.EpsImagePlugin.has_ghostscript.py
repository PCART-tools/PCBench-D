def has_ghostscript():
    if gs_windows_binary:
        return True
    if not sys.platform.startswith("win"):
        try:
            subprocess.check_call(["gs", "--version"], stdout=subprocess.DEVNULL)
            return True
        except OSError:
            # No Ghostscript
            pass
    return False
