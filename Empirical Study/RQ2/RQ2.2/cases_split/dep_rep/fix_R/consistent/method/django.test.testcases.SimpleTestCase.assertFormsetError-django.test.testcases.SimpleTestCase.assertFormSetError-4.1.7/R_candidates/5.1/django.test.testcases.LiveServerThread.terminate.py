    def terminate(self):
        if hasattr(self, "httpd"):
            # Stop the WSGI server
            self.httpd.shutdown()
            self.httpd.server_close()
        self.join()
