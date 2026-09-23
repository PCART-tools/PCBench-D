    def filter_cookies(self, request_url=URL()):
        """Returns this jar's cookies filtered by their attributes."""
        self._do_expiration()
        filtered = SimpleCookie()
        hostname = request_url.host or ""
        is_not_secure = request_url.scheme not in ("https", "wss")

        for cookie in self:
            name = cookie.key
            domain = cookie["domain"]

            # Send shared cookies
            if not domain:
                filtered[name] = cookie.value
                continue

            if not self._unsafe and is_ip_address(hostname):
                continue

            if (domain, name) in self._host_only_cookies:
                if domain != hostname:
                    continue
            elif not self._is_domain_match(domain, hostname):
                continue

            if not self._is_path_match(request_url.path, cookie["path"]):
                continue

            if is_not_secure and cookie["secure"]:
                continue

            filtered[name] = cookie.value

        return filtered
