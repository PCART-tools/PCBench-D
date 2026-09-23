    def _get_gui_framework_by_loading(self, backend):
        # Determine GUI framework for a backend by loading its module and reading the
        # FigureCanvas.required_interactive_framework attribute.
        # Returns "headless" if there is no GUI framework.
        module = self.load_backend_module(backend)
        canvas_class = module.FigureCanvas
        return canvas_class.required_interactive_framework or "headless"
