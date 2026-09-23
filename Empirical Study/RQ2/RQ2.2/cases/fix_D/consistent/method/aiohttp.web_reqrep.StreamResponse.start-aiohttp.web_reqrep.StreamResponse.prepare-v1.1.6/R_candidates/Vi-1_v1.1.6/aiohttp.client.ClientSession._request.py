    @asyncio.coroutine
    def _request(self, method, url, *,
                 params=None,
                 data=None,
                 headers=None,
                 skip_auto_headers=None,
                 auth=None,
                 allow_redirects=True,
                 max_redirects=10,
                 encoding='utf-8',
                 version=None,
                 compress=None,
                 chunked=None,
                 expect100=False,
                 read_until_eof=True,
                 proxy=None,
                 proxy_auth=None,
                 timeout=5*60):

        if version is not None:
            warnings.warn("HTTP version should be specified "
                          "by ClientSession constructor", DeprecationWarning)
        else:
            version = self._version

        if self.closed:
            raise RuntimeError('Session is closed')

        redirects = 0
        history = []

        # Merge with default headers and transform to CIMultiDict
        headers = self._prepare_headers(headers)
        if auth is None:
            auth = self._default_auth
        # It would be confusing if we support explicit Authorization header
        # with `auth` argument
        if (headers is not None and
                auth is not None and
                hdrs.AUTHORIZATION in headers):
            raise ValueError("Can't combine `Authorization` header with "
                             "`auth` argument")

        skip_headers = set(self._skip_auto_headers)
        if skip_auto_headers is not None:
            for i in skip_auto_headers:
                skip_headers.add(istr(i))

        if proxy is not None:
            proxy = URL(proxy)

        while True:
            url = URL(url).with_fragment(None)

            cookies = self._cookie_jar.filter_cookies(url)

            req = self._request_class(
                method, url, params=params, headers=headers,
                skip_auto_headers=skip_headers, data=data,
                cookies=cookies, encoding=encoding,
                auth=auth, version=version, compress=compress, chunked=chunked,
                expect100=expect100,
                loop=self._loop, response_class=self._response_class,
                proxy=proxy, proxy_auth=proxy_auth, timeout=timeout)

            with Timeout(timeout, loop=self._loop):
                conn = yield from self._connector.connect(req)
            conn.writer.set_tcp_nodelay(True)
            try:
                resp = req.send(conn.writer, conn.reader)
                try:
                    yield from resp.start(conn, read_until_eof)
                except:
                    resp.close()
                    conn.close()
                    raise
            except (aiohttp.HttpProcessingError,
                    aiohttp.ServerDisconnectedError) as exc:
                raise aiohttp.ClientResponseError() from exc
            except OSError as exc:
                raise aiohttp.ClientOSError(*exc.args) from exc

            self._cookie_jar.update_cookies(resp.cookies, resp.url_obj)

            # redirects
            if resp.status in (301, 302, 303, 307) and allow_redirects:
                redirects += 1
                history.append(resp)
                if max_redirects and redirects >= max_redirects:
                    resp.close()
                    break
                else:
                    # TODO: close the connection if BODY is large enough
                    # Redirect with big BODY is forbidden by HTTP protocol
                    # but malformed server may send illegal response.
                    # Small BODIES with text like "Not Found" are still
                    # perfectly fine and should be accepted.
                    yield from resp.release()

                # For 301 and 302, mimic IE behaviour, now changed in RFC.
                # Details: https://github.com/kennethreitz/requests/pull/269
                if (resp.status == 303 and resp.method != hdrs.METH_HEAD) \
                   or (resp.status in (301, 302) and
                       resp.method == hdrs.METH_POST):
                    method = hdrs.METH_GET
                    data = None
                    if headers.get(hdrs.CONTENT_LENGTH):
                        headers.pop(hdrs.CONTENT_LENGTH)

                r_url = (resp.headers.get(hdrs.LOCATION) or
                         resp.headers.get(hdrs.URI))
                if r_url is None:
                    raise RuntimeError("{0.method} {0.url_obj} returns "
                                       "a redirect [{0.status}] status "
                                       "but response lacks a Location "
                                       "or URI HTTP header".format(resp))
                r_url = URL(r_url)

                scheme = r_url.scheme
                if scheme not in ('http', 'https', ''):
                    resp.close()
                    raise ValueError('Can redirect only to http or https')
                elif not scheme:
                    r_url = url.join(r_url)

                url = r_url
                params = None
                yield from resp.release()
                continue

            break

        resp._history = tuple(history)
        return resp
