    def _validate_and_store_entry_points(self, entries):
        # Validate and store entry points so that they can be used via matplotlib.use()
        # in the normal manner. Entry point names cannot be of module:// format, cannot
        # shadow a built-in backend name, and there cannot be multiple entry points
        # with the same name but different modules. Multiple entry points with the same
        # name and value are permitted (it can sometimes happen outside of our control,
        # see https://github.com/matplotlib/matplotlib/issues/28367).
        for name, module in set(entries):
            name = name.lower()
            if name.startswith("module://"):
                raise RuntimeError(
                    f"Entry point name '{name}' cannot start with 'module://'")
            if name in self._BUILTIN_BACKEND_TO_GUI_FRAMEWORK:
                raise RuntimeError(f"Entry point name '{name}' is a built-in backend")
            if name in self._backend_to_gui_framework:
                raise RuntimeError(f"Entry point name '{name}' duplicated")

            self._name_to_module[name] = "module://" + module
            # Do not yet know backend GUI framework, determine it only when necessary.
            self._backend_to_gui_framework[name] = "unknown"
