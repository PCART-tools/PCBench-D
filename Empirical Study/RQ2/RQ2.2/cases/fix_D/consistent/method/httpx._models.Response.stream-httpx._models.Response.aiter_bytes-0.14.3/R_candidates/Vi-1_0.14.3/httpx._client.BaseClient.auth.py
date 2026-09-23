    @auth.setter
    def auth(self, auth: AuthTypes) -> None:
        self._auth = self._build_auth(auth)
