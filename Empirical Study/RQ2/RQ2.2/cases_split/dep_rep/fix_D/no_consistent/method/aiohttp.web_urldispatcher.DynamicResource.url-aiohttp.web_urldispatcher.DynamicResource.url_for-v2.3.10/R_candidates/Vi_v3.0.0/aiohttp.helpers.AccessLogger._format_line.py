    def _format_line(self, request, response, time):
        return ((key, method(request, response, time))
                for key, method in self._methods)
