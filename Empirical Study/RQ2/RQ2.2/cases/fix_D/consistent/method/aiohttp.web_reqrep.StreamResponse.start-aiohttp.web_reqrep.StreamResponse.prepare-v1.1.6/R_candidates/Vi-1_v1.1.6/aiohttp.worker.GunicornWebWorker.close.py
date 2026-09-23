    @asyncio.coroutine
    def close(self):
        if self.servers:
            servers = self.servers
            self.servers = None

            # stop accepting connections
            for server, handler in servers.items():
                self.log.info("Stopping server: %s, connections: %s",
                              self.pid, len(handler.connections))
                server.close()
                yield from server.wait_closed()

            # send on_shutdown event
            yield from self.wsgi.shutdown()

            # stop alive connections
            tasks = [
                handler.finish_connections(
                    timeout=self.cfg.graceful_timeout / 100 * 95)
                for handler in servers.values()]
            yield from asyncio.gather(*tasks, loop=self.loop)

            # cleanup application
            yield from self.wsgi.cleanup()
