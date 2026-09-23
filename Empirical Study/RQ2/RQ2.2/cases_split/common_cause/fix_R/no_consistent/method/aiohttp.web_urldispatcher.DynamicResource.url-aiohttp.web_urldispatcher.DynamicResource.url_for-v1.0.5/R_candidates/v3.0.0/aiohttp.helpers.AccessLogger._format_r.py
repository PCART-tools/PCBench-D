    @staticmethod
    def _format_r(request, response, time):
        if request is None:
            return '-'
        return '%s %s HTTP/%s.%s' % tuple((request.method,
                                           request.path_qs) + request.version)
