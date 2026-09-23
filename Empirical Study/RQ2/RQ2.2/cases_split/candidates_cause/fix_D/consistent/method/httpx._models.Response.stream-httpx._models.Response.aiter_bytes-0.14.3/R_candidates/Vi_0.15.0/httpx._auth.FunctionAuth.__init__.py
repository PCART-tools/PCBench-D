    def __init__(self, func: typing.Callable[[Request], Request]) -> None:
        self._func = func
