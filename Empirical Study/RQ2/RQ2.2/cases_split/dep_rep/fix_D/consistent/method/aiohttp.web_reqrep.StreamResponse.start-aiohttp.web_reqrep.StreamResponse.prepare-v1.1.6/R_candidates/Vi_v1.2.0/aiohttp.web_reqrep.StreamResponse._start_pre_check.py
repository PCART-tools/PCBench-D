    def _start_pre_check(self, request):
        if self._resp_impl is not None:
            if self._req is not request:
                raise RuntimeError(
                    "Response has been started with different request.")
            else:
                return self._resp_impl
        else:
            return None
