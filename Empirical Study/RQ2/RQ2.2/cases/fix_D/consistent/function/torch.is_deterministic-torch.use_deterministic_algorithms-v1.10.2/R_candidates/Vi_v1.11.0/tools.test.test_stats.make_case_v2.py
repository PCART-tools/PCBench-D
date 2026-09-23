def make_case_v2(seconds: float, status: Status = None) -> Version2Case:
    return {
        'seconds': seconds,
        'status': status,
    }
