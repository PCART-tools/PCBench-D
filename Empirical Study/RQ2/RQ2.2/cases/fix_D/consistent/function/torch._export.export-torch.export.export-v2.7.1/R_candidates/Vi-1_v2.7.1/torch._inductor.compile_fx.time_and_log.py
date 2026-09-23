    def time_and_log(attr: str) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:
        return dynamo_utils.identity
