class URL:
    """
    url = httpx.URL("HTTPS://jo%40email.com:a%20secret@example.com:1234/pa%20th?search=ab#anchorlink")

    assert url.scheme == "https"
    assert url.username == "jo@email.com"
    assert url.password == "a secret"
    assert url.userinfo == b"jo%40email.com:a%20secret"
    assert url.host == "example.com"
    assert url.port == 1234
    assert url.netloc == "example.com:1234"
    assert url.path == "/pa th"
    assert url.query == b"?search=ab"
    assert url.raw_path == b"/pa%20th?search=ab"
    assert url.fragment == "anchorlink"

    The components of a URL are broken down like this:

    https://jo%40email.com:a%20secret@example.com:1234/pa%20th?search=ab#anchorlink
    [scheme][  username  ] [password] [  host  ][port][ path ] [ query ] [fragment]
            [       userinfo        ] [    netloc    ][    raw_path    ]

    Note that:

    * `url.scheme` is normalized to always be lowercased.

    * `url.host` is normalized to always be lowercased, and is IDNA encoded. For instance:
       url = httpx.URL("http://中国.icom.museum")
       assert url.host == "xn--fiqs8s.icom.museum"

    * `url.userinfo` is raw bytes, without URL escaping. Usually you'll want to work with
      `url.username` and `url.password` instead, which handle the URL escaping.

    * `url.raw_path` is raw bytes of both the path and query, without URL escaping.
      This portion is used as the target when constructing HTTP requests. Usually you'll
      want to work with `url.path` instead.

    * `url.query` is raw bytes, without URL escaping. A URL query string portion can only
      be properly URL escaped when decoding the parameter names and values themselves.
    """

    def __init__(
        self, url: typing.Union["URL", str, RawURL] = "", params: QueryParamTypes = None
    ) -> None:
        if isinstance(url, (str, tuple)):
            if isinstance(url, tuple):
                raw_scheme, raw_host, port, raw_path = url
                scheme = raw_scheme.decode("ascii")
                host = raw_host.decode("ascii")
                port_str = "" if port is None else f":{port}"
                path = raw_path.decode("ascii")
                url = f"{scheme}://{host}{port_str}{path}"

            try:
                self._uri_reference = rfc3986.iri_reference(url).encode()
            except rfc3986.exceptions.InvalidAuthority as exc:
                raise InvalidURL(message=str(exc)) from None

            if self.is_absolute_url:
                # We don't want to normalize relative URLs, since doing so
                # removes any leading `../` portion.
                self._uri_reference = self._uri_reference.normalize()
        elif isinstance(url, URL):
            self._uri_reference = url._uri_reference
        else:
            raise TypeError(
                f"Invalid type for url.  Expected str or httpx.URL, got {type(url)}"
            )

        # Add any query parameters, merging with any in the URL if needed.
        if params:
            if self._uri_reference.query:
                url_params = QueryParams(self._uri_reference.query)
                url_params.update(params)
                query_string = str(url_params)
            else:
                query_string = str(QueryParams(params))
            self._uri_reference = self._uri_reference.copy_with(query=query_string)

    @property
    def scheme(self) -> str:
        """
        The URL scheme, such as "http", "https".
        Always normalised to lowercase.
        """
        return self._uri_reference.scheme or ""

    @property
    def userinfo(self) -> bytes:
        """
        The URL userinfo as a raw bytestring.
        For example: b"jo%40email.com:a%20secret".
        """
        userinfo = self._uri_reference.userinfo or ""
        return userinfo.encode("ascii")

    @property
    def username(self) -> str:
        """
        The URL username as a string, with URL decoding applied.
        For example: "jo@email.com"
        """
        userinfo = self._uri_reference.userinfo or ""
        return unquote(userinfo.partition(":")[0])

    @property
    def password(self) -> str:
        """
        The URL password as a string, with URL decoding applied.
        For example: "a secret"
        """
        userinfo = self._uri_reference.userinfo or ""
        return unquote(userinfo.partition(":")[2])

    @property
    def host(self) -> str:
        """
        The URL host as a string.
        Always normlized to lowercase, and IDNA encoded.

        Examples:

        url = httpx.URL("http://www.EXAMPLE.org")
        assert url.host == "www.example.org"

        url = httpx.URL("http://中国.icom.museum")
        assert url.host == "xn--fiqs8s.icom.museum"
        """
        return self._uri_reference.host or ""

    @property
    def port(self) -> typing.Optional[int]:
        """
        The URL port as an integer.
        """
        port = self._uri_reference.port
        return int(port) if port else None

    @property
    def netloc(self) -> str:
        """
        Either `<host>` or `<host>:<port>` as a string.
        Always normlized to lowercase, and IDNA encoded.
        """
        host = self._uri_reference.host or ""
        port = self._uri_reference.port
        return host if port is None else f"{host}:{port}"

    @property
    def path(self) -> str:
        """
        The URL path as a string. Excluding the query string, and URL decoded.

        For example:

        url = httpx.URL("https://example.com/pa%20th")
        assert url.path == "/pa th"
        """
        path = self._uri_reference.path or "/"
        return unquote(path)

    @property
    def query(self) -> bytes:
        """
        The URL query string, as raw bytes, excluding the leading b"?".
        Note that URL decoding can only be applied on URL query strings
        at the point of decoding the individual parameter names/values.
        """
        query = self._uri_reference.query or ""
        return query.encode("ascii")

    @property
    def raw_path(self) -> bytes:
        """
        The complete URL path and query string as raw bytes.
        Used as the target when constructing HTTP requests.

        For example:

        GET /users?search=some%20text HTTP/1.1
        Host: www.example.org
        Connection: close
        """
        path = self._uri_reference.path or "/"
        if self._uri_reference.query is not None:
            path += "?" + self._uri_reference.query
        return path.encode("ascii")

    @property
    def fragment(self) -> str:
        """
        The URL fragments, as used in HTML anchors.
        As a string, without the leading '#'.
        """
        return self._uri_reference.fragment or ""

    @property
    def raw(self) -> RawURL:
        """
        The URL in the raw representation used by the low level
        transport API. For example, see `httpcore`.

        Provides the (scheme, host, port, target) for the outgoing request.
        """
        return (
            self.scheme.encode("ascii"),
            self.host.encode("ascii"),
            self.port,
            self.raw_path,
        )

    @property
    def is_absolute_url(self) -> bool:
        """
        Return `True` for absolute URLs such as 'http://example.com/path',
        and `False` for relative URLs such as '/path'.
        """
        # We don't use `.is_absolute` from `rfc3986` because it treats
        # URLs with a fragment portion as not absolute.
        # What we actually care about is if the URL provides
        # a scheme and hostname to which connections should be made.
        return bool(self.scheme and self.host)

    @property
    def is_relative_url(self) -> bool:
        """
        Return `False` for absolute URLs such as 'http://example.com/path',
        and `True` for relative URLs such as '/path'.
        """
        return not self.is_absolute_url

    def copy_with(self, **kwargs: typing.Any) -> "URL":
        """
        Copy this URL, returning a new URL with some components altered.
        Accepts the same set of parameters as the components that are made
        available via properties on the `URL` class.

        For example:

        url = httpx.URL("https://www.example.com").copy_with(username="jo@gmail.com", password="a secret")
        assert url == "https://jo%40email.com:a%20secret@www.example.com"
        """
        allowed = {
            "scheme": str,
            "username": str,
            "password": str,
            "userinfo": bytes,
            "host": str,
            "port": int,
            "netloc": str,
            "path": str,
            "query": bytes,
            "raw_path": bytes,
            "fragment": str,
        }
        for key, value in kwargs.items():
            if key not in allowed:
                message = f"{key!r} is an invalid keyword argument for copy_with()"
                raise TypeError(message)
            if value is not None and not isinstance(value, allowed[key]):
                expected = allowed[key].__name__
                seen = type(value).__name__
                message = f"Argument {key!r} must be {expected} but got {seen}"
                raise TypeError(message)

        # Replace username, password, userinfo, host, port, netloc with "authority" for rfc3986
        if "username" in kwargs or "password" in kwargs:
            # Consolidate username and password into userinfo.
            username = quote(kwargs.pop("username", self.username) or "")
            password = quote(kwargs.pop("password", self.password) or "")
            userinfo = f"{username}:{password}" if password else username
            kwargs["userinfo"] = userinfo.encode("ascii")

        if "host" in kwargs or "port" in kwargs:
            # Consolidate host and port into  netloc.
            host = kwargs.pop("host", self.host) or ""
            port = kwargs.pop("port", self.port)
            kwargs["netloc"] = f"{host}:{port}" if port is not None else host

        if "userinfo" in kwargs or "netloc" in kwargs:
            # Consolidate userinfo and netloc into authority.
            userinfo = (kwargs.pop("userinfo", self.userinfo) or b"").decode("ascii")
            netloc = kwargs.pop("netloc", self.netloc) or ""
            authority = f"{userinfo}@{netloc}" if userinfo else netloc
            kwargs["authority"] = authority

        if "raw_path" in kwargs:
            raw_path = kwargs.pop("raw_path") or b""
            path, has_query, query = raw_path.decode("ascii").partition("?")
            kwargs["path"] = path
            kwargs["query"] = query if has_query else None

        else:
            # Ensure path=<url quoted str> for rfc3986
            if kwargs.get("path") is not None:
                kwargs["path"] = quote(kwargs["path"])

            # Ensure query=<str> for rfc3986
            if kwargs.get("query") is not None:
                kwargs["query"] = kwargs["query"].decode("ascii")

        return URL(self._uri_reference.copy_with(**kwargs).unsplit())

    def join(self, url: URLTypes) -> "URL":
        """
        Return an absolute URL, using this URL as the base.

        Eg.

        url = httpx.URL("https://www.example.com/test")
        url = url.join("/new/path")
        assert url == "https://www.example.com/test/new/path"
        """
        if self.is_relative_url:
            return URL(url)

        # We drop any fragment portion, because RFC 3986 strictly
        # treats URLs with a fragment portion as not being absolute URLs.
        base_uri = self._uri_reference.copy_with(fragment=None)
        relative_url = URL(url)
        return URL(relative_url._uri_reference.resolve_with(base_uri).unsplit())

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: typing.Any) -> bool:
        return isinstance(other, (URL, str)) and str(self) == str(other)

    def __str__(self) -> str:
        return self._uri_reference.unsplit()

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        url_str = str(self)
        if self._uri_reference.userinfo:
            username = quote(self.username)
            url_str = (
                rfc3986.urlparse(url_str)
                .copy_with(userinfo=f"{username}:[secure]")
                .unsplit()
            )
        return f"{class_name}({url_str!r})"
