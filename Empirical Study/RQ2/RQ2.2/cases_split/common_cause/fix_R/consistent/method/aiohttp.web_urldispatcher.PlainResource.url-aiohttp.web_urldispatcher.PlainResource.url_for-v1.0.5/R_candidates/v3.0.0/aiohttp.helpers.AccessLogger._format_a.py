    @staticmethod
    def _format_a(request, response, time):
        if request is None:
            return '-'
        ip = request.remote
        return ip if ip is not None else '-'
