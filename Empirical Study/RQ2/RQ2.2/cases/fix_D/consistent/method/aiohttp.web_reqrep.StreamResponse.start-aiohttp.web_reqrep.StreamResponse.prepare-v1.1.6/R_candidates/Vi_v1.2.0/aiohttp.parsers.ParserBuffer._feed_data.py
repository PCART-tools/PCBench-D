    @staticmethod
    def _feed_data(helper):
        while True:
            chunk = yield
            if chunk:
                helper.data.extend(chunk)

            if helper.exception:
                raise helper.exception
