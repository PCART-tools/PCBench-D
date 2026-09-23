    def configure(self, options, conf):
        if not self.can_configure:
            return

        self.enabled = getattr(options, 'performGC', False)
