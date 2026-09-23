    @classmethod
    @functools.lru_cache()
    def _fix_ipython_backend2gui(cls):
        # Fix hard-coded module -> toolkit mapping in IPython (used for
        # `ipython --auto`).  This cannot be done at import time due to
        # ordering issues, so we do it when creating a canvas, and should only
        # be done once per class (hence the `lru_cache(1)`).
        if sys.modules.get("IPython") is None:
            return
        import IPython
        ip = IPython.get_ipython()
        if not ip:
            return
        from IPython.core import pylabtools as pt
        if (not hasattr(pt, "backend2gui")
                or not hasattr(ip, "enable_matplotlib")):
            # In case we ever move the patch to IPython and remove these APIs,
            # don't break on our side.
            return
        backend2gui_rif = {
            "qt": "qt",
            "gtk3": "gtk3",
            "gtk4": "gtk4",
            "wx": "wx",
            "macosx": "osx",
        }.get(cls.required_interactive_framework)
        if backend2gui_rif:
            if _is_non_interactive_terminal_ipython(ip):
                ip.enable_gui(backend2gui_rif)
