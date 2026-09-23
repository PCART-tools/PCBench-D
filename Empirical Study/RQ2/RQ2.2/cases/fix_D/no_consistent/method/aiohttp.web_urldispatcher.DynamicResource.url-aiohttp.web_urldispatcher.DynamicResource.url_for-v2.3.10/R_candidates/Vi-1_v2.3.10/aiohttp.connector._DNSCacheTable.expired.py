    def expired(self, host):
        if self._ttl is None:
            return False

        return (
            self._timestamps[host] + self._ttl
        ) < monotonic()
