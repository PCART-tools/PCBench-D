    @staticmethod
    def _format_i(key, request, response, time):
        if request is None:
            return '(no headers)'

        # suboptimal, make istr(key) once
        return request.headers.get(key, '-')
