    def _prepare_middleware(self):
        for m in reversed(self._middlewares):
            if getattr(m, '__middleware_version__', None) == 1:
                yield m, True
            else:
                warnings.warn('old-style middleware "{!r}" deprecated, '
                              'see #2252'.format(m),
                              DeprecationWarning, stacklevel=2)
                yield m, False

        yield _fix_request_current_app(self), True
