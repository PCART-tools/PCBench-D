    def run(self):
        if hasattr(self.wsgi, 'startup'):
            self.loop.run_until_complete(self.wsgi.startup())
        self._runner = ensure_future(self._run(), loop=self.loop)

        try:
            self.loop.run_until_complete(self._runner)
        finally:
            if hasattr(self.loop, 'shutdown_asyncgens'):
                self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            self.loop.close()

        sys.exit(self.exit_code)
