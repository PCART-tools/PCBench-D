    def _initialize_colspace(self, col_space: ColspaceArgType | None) -> ColspaceType:
        result: ColspaceType

        if col_space is None:
            result = {}
        elif isinstance(col_space, (int, str)):
            result = {"": col_space}
            result.update({column: col_space for column in self.frame.columns})
        elif isinstance(col_space, Mapping):
            for column in col_space.keys():
                if column not in self.frame.columns and column != "":
                    raise ValueError(
                        f"Col_space is defined for an unknown column: {column}"
                    )
            result = col_space
        else:
            if len(self.frame.columns) != len(col_space):
                raise ValueError(
                    f"Col_space length({len(col_space)}) should match "
                    f"DataFrame number of columns({len(self.frame.columns)})"
                )
            result = dict(zip(self.frame.columns, col_space))
        return result
