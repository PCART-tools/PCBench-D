    def validate(cls, value: Path) -> Path:
        if not value.is_file():
            raise errors.PathNotAFileError(path=value)

        return value
