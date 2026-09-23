    def update_cookies(self, cookies, response_url=URL()):
        """Update cookies."""
        hostname = response_url.host

        if not self._unsafe and is_ip_address(hostname):
            # Don't accept cookies from IPs
            return

        if isinstance(cookies, Mapping):
            cookies = cookies.items()

        for name, cookie in cookies:
            if not isinstance(cookie, Morsel):
                tmp = SimpleCookie()
                tmp[name] = cookie
                cookie = tmp[name]

            domain = cookie["domain"]

            # ignore domains with trailing dots
            if domain.endswith('.'):
                domain = ""
                del cookie["domain"]

            if not domain and hostname is not None:
                # Set the cookie's domain to the response hostname
                # and set its host-only-flag
                self._host_only_cookies.add((hostname, name))
                domain = cookie["domain"] = hostname

            if domain.startswith("."):
                # Remove leading dot
                domain = domain[1:]
                cookie["domain"] = domain

            if hostname and not self._is_domain_match(domain, hostname):
                # Setting cookies for different domains is not allowed
                continue

            path = cookie["path"]
            if not path or not path.startswith("/"):
                # Set the cookie's path to the response path
                path = response_url.path
                if not path.startswith("/"):
                    path = "/"
                else:
                    # Cut everything from the last slash to the end
                    path = "/" + path[1:path.rfind("/")]
                cookie["path"] = path

            max_age = cookie["max-age"]
            if max_age:
                try:
                    delta_seconds = int(max_age)
                    self._expire_cookie(self._loop.time() + delta_seconds,
                                        domain, name)
                except ValueError:
                    cookie["max-age"] = ""

            else:
                expires = cookie["expires"]
                if expires:
                    expire_time = self._parse_date(expires)
                    if expire_time:
                        self._expire_cookie(expire_time.timestamp(),
                                            domain, name)
                    else:
                        cookie["expires"] = ""

            # use dict method because SimpleCookie class modifies value
            # before Python 3.4.3
            dict.__setitem__(self._cookies[domain], name, cookie)

        self._do_expiration()
