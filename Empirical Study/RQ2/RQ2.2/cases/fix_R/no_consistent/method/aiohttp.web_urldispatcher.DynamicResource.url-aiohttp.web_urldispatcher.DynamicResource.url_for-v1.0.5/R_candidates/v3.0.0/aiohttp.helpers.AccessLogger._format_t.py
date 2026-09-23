    @staticmethod
    def _format_t(request, response, time):
        now = datetime.datetime.utcnow()
        start_time = now - datetime.timedelta(seconds=time)
        return start_time.strftime('[%d/%b/%Y:%H:%M:%S +0000]')
