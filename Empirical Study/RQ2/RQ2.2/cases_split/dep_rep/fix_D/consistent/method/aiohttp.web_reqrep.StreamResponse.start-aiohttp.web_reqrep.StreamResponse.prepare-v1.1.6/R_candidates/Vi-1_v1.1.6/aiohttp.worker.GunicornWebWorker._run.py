    @asyncio.coroutine
    def _run(self):

        ctx = self._create_ssl_context(self.cfg) if self.cfg.is_ssl else None

        for sock in self.sockets:
            handler = self.make_handler(self.wsgi)

            if hasattr(socket, 'AF_UNIX') and sock.family == socket.AF_UNIX:
                srv = yield from self.loop.create_unix_server(
                    handler, sock=sock.sock, ssl=ctx)
            else:
                srv = yield from self.loop.create_server(
                    handler, sock=sock.sock, ssl=ctx)
            self.servers[srv] = handler

        # If our parent changed then we shut down.
        pid = os.getpid()
        try:
            while self.alive:
                self.notify()

                cnt = sum(handler.requests_count
                          for handler in self.servers.values())
                if self.cfg.max_requests and cnt > self.cfg.max_requests:
                    self.alive = False
                    self.log.info("Max requests, shutting down: %s", self)

                elif pid == os.getpid() and self.ppid != os.getppid():
                    self.alive = False
                    self.log.info("Parent changed, shutting down: %s", self)
                else:
                    yield from asyncio.sleep(1.0, loop=self.loop)

        except BaseException:
            pass

        yield from self.close()
