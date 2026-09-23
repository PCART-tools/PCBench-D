    def set_transport(self, transport):
        assert transport is None or self.transport is None, \
            'Transport already set'
        self.transport = transport
