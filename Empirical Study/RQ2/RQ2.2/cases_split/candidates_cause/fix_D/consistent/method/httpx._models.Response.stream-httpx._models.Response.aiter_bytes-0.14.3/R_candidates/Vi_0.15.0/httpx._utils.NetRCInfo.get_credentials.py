    def get_credentials(self, host: str) -> typing.Optional[typing.Tuple[str, str]]:
        if self.netrc_info is None:
            return None

        auth_info = self.netrc_info.authenticators(host)
        if auth_info is None or auth_info[2] is None:
            return None
        return (auth_info[0], auth_info[2])
