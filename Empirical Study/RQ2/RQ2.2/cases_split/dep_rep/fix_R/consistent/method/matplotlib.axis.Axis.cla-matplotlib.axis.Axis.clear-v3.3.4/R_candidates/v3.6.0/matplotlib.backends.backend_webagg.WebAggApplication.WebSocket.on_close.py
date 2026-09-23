        def on_close(self):
            self.manager.remove_web_socket(self)
