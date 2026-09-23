    def __repr__(self) -> str:
        # don't expose internal/private classpath
        width = self.width
        cols_str = "{} col{}".format(width, "" if width == 1 else "s")
        schema_max_2 = (
            item for i, item in enumerate(self.schema.items()) if i in (0, width - 1)
        )
        schema_str = (", " if width == 2 else " … ").join(
            (f'"{k}": {v}' for k, v in schema_max_2)
        )
        return f"<{self.__class__.__name__} [{cols_str}, {{{schema_str}}}] at 0x{id(self):X}>"
