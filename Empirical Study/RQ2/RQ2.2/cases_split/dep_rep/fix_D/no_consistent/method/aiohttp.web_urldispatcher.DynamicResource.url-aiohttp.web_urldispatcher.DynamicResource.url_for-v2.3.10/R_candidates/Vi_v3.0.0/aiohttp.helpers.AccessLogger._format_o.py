    @staticmethod
    def _format_o(key, request, response, time):
        # suboptimal, make istr(key) once
        return response.headers.get(key, '-')
