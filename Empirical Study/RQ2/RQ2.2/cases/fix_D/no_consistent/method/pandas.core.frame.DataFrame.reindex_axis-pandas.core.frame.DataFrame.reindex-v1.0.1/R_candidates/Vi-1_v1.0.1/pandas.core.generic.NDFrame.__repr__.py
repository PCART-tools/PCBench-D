    def __repr__(self) -> str:
        # string representation based upon iterating over self
        # (since, by definition, `PandasContainers` are iterable)
        prepr = f"[{','.join(map(pprint_thing, self))}]"
        return f"{type(self).__name__}({prepr})"
