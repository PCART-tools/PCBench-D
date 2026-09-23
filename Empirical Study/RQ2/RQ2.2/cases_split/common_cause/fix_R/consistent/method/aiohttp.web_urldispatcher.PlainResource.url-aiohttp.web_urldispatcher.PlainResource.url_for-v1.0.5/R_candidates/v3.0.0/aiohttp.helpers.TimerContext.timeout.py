    def timeout(self):
        if not self._cancelled:
            for task in set(self._tasks):
                task.cancel()

            self._cancelled = True
