    def interpolate(self: T, inplace: bool, **kwargs) -> T:
        return self.apply(
            "interpolate", inplace=inplace, **kwargs, using_cow=using_copy_on_write()
        )
