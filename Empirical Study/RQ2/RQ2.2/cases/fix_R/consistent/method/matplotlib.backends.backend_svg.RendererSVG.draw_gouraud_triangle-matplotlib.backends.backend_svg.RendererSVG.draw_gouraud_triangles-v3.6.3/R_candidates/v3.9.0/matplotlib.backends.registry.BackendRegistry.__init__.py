    def __init__(self):
        # Only load entry points when first needed.
        self._loaded_entry_points = False

        # Mapping of non-built-in backend to GUI framework, added dynamically from
        # entry points and from matplotlib.use("module://some.backend") format.
        # New entries have an "unknown" GUI framework that is determined when first
        # needed by calling _get_gui_framework_by_loading.
        self._backend_to_gui_framework = {}

        # Mapping of backend name to module name, where different from
        # f"matplotlib.backends.backend_{backend_name.lower()}". These are either
        # hardcoded for backward compatibility, or loaded from entry points or
        # "module://some.backend" syntax.
        self._name_to_module = {
            "notebook": "nbagg",
        }
