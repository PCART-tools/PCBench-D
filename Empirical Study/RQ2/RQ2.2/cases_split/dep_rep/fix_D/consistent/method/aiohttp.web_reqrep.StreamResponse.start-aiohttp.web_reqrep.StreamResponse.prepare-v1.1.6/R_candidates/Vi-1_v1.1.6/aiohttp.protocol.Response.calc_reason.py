    @staticmethod
    def calc_reason(status, *, _RESPONSES=RESPONSES):
        record = _RESPONSES.get(status)
        if record is not None:
            reason = record[0]
        else:
            reason = str(status)
        return reason
