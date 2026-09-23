    def getlist(self, key: typing.Any) -> typing.List[str]:
        message = (
            "QueryParams.getlist() is pending deprecation. Use QueryParams.get_list()"
        )
        warnings.warn(message, DeprecationWarning)
        return self.get_list(key)
