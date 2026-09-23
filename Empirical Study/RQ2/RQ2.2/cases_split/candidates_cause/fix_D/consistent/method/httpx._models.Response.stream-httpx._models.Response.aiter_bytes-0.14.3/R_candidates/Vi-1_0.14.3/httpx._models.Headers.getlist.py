    def getlist(self, key: str, split_commas: bool = False) -> typing.List[str]:
        message = "Headers.getlist() is pending deprecation. Use Headers.get_list()"
        warnings.warn(message, DeprecationWarning)
        return self.get_list(key, split_commas=split_commas)
