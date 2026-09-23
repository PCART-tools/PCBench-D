    @staticmethod
    def _format_t(request, response, time):
        return datetime.datetime.utcnow().strftime('[%d/%b/%Y:%H:%M:%S +0000]')
