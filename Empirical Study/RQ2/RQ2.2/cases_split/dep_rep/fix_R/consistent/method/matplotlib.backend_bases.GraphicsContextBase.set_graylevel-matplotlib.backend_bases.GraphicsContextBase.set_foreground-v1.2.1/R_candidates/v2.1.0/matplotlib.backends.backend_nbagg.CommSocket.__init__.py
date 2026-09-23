    def __init__(self, manager):
        self.supports_binary = None
        self.manager = manager
        self.uuid = str(uuid())
        # Publish an output area with a unique ID. The javascript can then
        # hook into this area.
        display(HTML("<div id=%r></div>" % self.uuid))
        try:
            self.comm = Comm('matplotlib', data={'id': self.uuid})
        except AttributeError:
            raise RuntimeError('Unable to create an IPython notebook Comm '
                               'instance. Are you in the IPython notebook?')
        self.comm.on_msg(self.on_message)

        manager = self.manager
        self._ext_close = False

        def _on_close(close_message):
            self._ext_close = True
            manager.remove_comm(close_message['content']['comm_id'])
            manager.clearup_closed()

        self.comm.on_close(_on_close)
