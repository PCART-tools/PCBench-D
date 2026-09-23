    @staticmethod
    def handle_kwargs(kwargs: Dict) -> List:
        if len(kwargs) == 1:
            output = list(kwargs.values())
        else:
            output = list(chain(kwargs.values()))

        return DefaultArgumentHandler.handle_args(output)
