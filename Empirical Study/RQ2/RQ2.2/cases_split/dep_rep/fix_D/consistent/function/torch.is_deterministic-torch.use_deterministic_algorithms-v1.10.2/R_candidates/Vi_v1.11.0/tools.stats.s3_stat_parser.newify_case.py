def newify_case(case: Version1Case) -> Version2Case:
    return {
        'seconds': case['seconds'],
        'status': case_status(case),
    }
