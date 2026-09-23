    @staticmethod
    def handle_args(args: Sequence[Any]) -> List[str]:

        # Only one argument, let's do case by case
        if len(args) == 1:
            if isinstance(args[0], str):
                return [args[0]]
            elif not isinstance(args[0], list):
                return list(args)
            else:
                return args[0]

        # Multiple arguments (x1, x2, ...)
        elif len(args) > 1:
            if all([isinstance(arg, str) for arg in args]):
                return list(args)

            # If not instance of list, then it should instance of iterable
            elif isinstance(args, Iterable):
                return list(chain.from_iterable(chain(args)))
            else:
                raise ValueError(
                    "Invalid input type {}. Pipeline supports Union[str, Iterable[str]]".format(type(args))
                )
        else:
            return []
