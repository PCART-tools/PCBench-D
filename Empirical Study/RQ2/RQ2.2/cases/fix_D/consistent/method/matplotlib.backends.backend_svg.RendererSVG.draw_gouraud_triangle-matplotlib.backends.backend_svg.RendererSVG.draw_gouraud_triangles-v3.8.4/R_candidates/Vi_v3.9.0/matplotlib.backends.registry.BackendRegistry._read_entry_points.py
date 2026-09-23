    def _read_entry_points(self):
        # Read entry points of modules that self-advertise as Matplotlib backends.
        # Expects entry points like this one from matplotlib-inline (in pyproject.toml
        # format):
        #   [project.entry-points."matplotlib.backend"]
        #   inline = "matplotlib_inline.backend_inline"
        import importlib.metadata as im
        import sys

        # entry_points group keyword not available before Python 3.10
        group = "matplotlib.backend"
        if sys.version_info >= (3, 10):
            entry_points = im.entry_points(group=group)
        else:
            entry_points = im.entry_points().get(group, ())
        entries = [(entry.name, entry.value) for entry in entry_points]

        # For backward compatibility, if matplotlib-inline and/or ipympl are installed
        # but too old to include entry points, create them. Do not import ipympl
        # directly as this calls matplotlib.use() whilst in this function.
        def backward_compatible_entry_points(
                entries, module_name, threshold_version, names, target):
            from matplotlib import _parse_to_version_info
            try:
                module_version = im.version(module_name)
                if _parse_to_version_info(module_version) < threshold_version:
                    for name in names:
                        entries.append((name, target))
            except im.PackageNotFoundError:
                pass

        names = [entry[0] for entry in entries]
        if "inline" not in names:
            backward_compatible_entry_points(
                entries, "matplotlib_inline", (0, 1, 7), ["inline"],
                "matplotlib_inline.backend_inline")
        if "ipympl" not in names:
            backward_compatible_entry_points(
                entries, "ipympl", (0, 9, 4), ["ipympl", "widget"],
                "ipympl.backend_nbagg")

        return entries
