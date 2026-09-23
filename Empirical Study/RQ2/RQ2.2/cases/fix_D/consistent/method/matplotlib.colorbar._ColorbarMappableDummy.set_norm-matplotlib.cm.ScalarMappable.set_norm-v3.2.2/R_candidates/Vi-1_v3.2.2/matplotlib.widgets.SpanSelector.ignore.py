    def ignore(self, event):
        # docstring inherited
        return _SelectorWidget.ignore(self, event) or not self.visible
