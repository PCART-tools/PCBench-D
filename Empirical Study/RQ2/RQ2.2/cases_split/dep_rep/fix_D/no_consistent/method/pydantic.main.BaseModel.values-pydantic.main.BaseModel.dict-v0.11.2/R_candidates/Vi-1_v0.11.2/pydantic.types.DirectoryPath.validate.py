    def validate(cls, value: Path) -> Path:
        if not value.is_dir():
            raise errors.PathNotADirectoryError(path=value)

        return value
