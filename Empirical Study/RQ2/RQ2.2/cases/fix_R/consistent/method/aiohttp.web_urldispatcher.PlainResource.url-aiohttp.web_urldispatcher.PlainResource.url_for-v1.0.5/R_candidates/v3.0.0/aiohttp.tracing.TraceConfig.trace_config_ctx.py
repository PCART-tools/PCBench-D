    def trace_config_ctx(self, trace_request_ctx=None):
        """ Return a new trace_config_ctx instance """
        return self._trace_config_ctx_factory(
            trace_request_ctx=trace_request_ctx)
