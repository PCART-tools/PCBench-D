    def _build_request_auth(
        self, request: Request, auth: typing.Union[AuthTypes, UnsetType] = UNSET
    ) -> Auth:
        auth = self._auth if isinstance(auth, UnsetType) else self._build_auth(auth)

        if auth is not None:
            return auth

        username, password = request.url.username, request.url.password
        if username or password:
            return BasicAuth(username=username, password=password)

        if self.trust_env and "Authorization" not in request.headers:
            credentials = self._netrc.get_credentials(request.url.host)
            if credentials is not None:
                return BasicAuth(username=credentials[0], password=credentials[1])

        return Auth()
