    def __enter__(self):
        if self._timeout is not None:
            self._task = current_task(loop=self._loop)
            if self._task is None:
                raise RuntimeError(
                    'Timeout context manager should be used inside a task')
            self._cancel_handler = self._loop.call_at(
                ceil(self._loop.time() + self._timeout), self._cancel_task)
        return self
