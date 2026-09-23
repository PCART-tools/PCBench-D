    def convert(self: T, copy: bool | None) -> T:
        if copy is None:
            if using_copy_on_write():
                copy = False
            else:
                copy = True
        elif using_copy_on_write():
            copy = False

        return self.apply("convert", copy=copy, using_cow=using_copy_on_write())
