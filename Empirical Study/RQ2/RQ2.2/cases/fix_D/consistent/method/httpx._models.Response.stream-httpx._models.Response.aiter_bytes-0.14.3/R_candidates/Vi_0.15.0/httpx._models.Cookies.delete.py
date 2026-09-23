    def delete(self, name: str, domain: str = None, path: str = None) -> None:
        """
        Delete a cookie by name. May optionally include domain and path
        in order to specify exactly which cookie to delete.
        """
        if domain is not None and path is not None:
            return self.jar.clear(domain, path, name)

        remove = []
        for cookie in self.jar:
            if cookie.name == name:
                if domain is None or cookie.domain == domain:
                    if path is None or cookie.path == path:
                        remove.append(cookie)

        for cookie in remove:
            self.jar.clear(cookie.domain, cookie.path, cookie.name)
