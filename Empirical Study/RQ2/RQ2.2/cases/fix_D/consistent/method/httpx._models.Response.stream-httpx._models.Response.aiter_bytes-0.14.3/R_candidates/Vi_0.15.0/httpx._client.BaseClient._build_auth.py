    def _build_auth(self, auth: AuthTypes) -> typing.Optional[Auth]:
        if auth is None:
            return None
        elif isinstance(auth, tuple):
            return BasicAuth(username=auth[0], password=auth[1])
        elif isinstance(auth, Auth):
            return auth
        elif callable(auth):
            return FunctionAuth(func=auth)
        else:
            raise TypeError('Invalid "auth" argument.')
