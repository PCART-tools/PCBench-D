    def _release_waiter(self):
        # always release only one waiter

        if self._limit:
            # if we have limit and we have available
            if self._limit - len(self._acquired) > 0:
                for key, waiters in self._waiters.items():
                    if waiters:
                        if not waiters[0].done():
                            waiters[0].set_result(None)
                        break

        elif self._limit_per_host:
            # if we have dont have limit but have limit per host
            # then release first available
            for key, waiters in self._waiters.items():
                if waiters:
                    if not waiters[0].done():
                        waiters[0].set_result(None)
                    break
