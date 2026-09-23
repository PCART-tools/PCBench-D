    def ignore(self, event):
        """return *True* if *event* should be ignored"""
        return _SelectorWidget.ignore(self, event) or not self.visible
