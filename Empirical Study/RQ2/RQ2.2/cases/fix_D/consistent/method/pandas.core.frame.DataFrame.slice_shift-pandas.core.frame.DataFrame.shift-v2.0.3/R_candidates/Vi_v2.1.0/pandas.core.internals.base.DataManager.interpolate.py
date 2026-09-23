    def interpolate(self, inplace: bool, **kwargs) -> Self:
        return self.apply_with_block(
            "interpolate", inplace=inplace, **kwargs, using_cow=using_copy_on_write()
        )
