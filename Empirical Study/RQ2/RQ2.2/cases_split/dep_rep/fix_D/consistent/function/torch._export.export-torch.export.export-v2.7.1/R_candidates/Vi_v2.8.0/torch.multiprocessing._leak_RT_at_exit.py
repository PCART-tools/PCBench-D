    def _leak_RT_at_exit():
        def _noop(x):
            pass

        _RT.__del__ = _noop  # type: ignore[attr-defined]
