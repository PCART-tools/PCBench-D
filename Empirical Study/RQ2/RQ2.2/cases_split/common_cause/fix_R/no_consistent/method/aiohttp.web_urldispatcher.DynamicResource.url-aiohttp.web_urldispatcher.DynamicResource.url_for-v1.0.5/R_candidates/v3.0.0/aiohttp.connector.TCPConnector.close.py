    def close(self):
        """Close all ongoing DNS calls."""
        for ev in self._throttle_dns_events.values():
            ev.cancel()

        super().close()
