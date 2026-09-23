def sort_by_number_of_args(declaration: Declaration, reverse: bool = True) -> None:
    def num_args(option: Option) -> int:
        return len(option['arguments'])
    declaration['options'].sort(key=num_args, reverse=reverse)
