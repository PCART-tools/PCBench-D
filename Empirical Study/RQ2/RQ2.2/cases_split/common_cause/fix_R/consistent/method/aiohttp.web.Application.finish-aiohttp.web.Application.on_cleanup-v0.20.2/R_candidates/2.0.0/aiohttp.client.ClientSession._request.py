    @asyncio.coroutine
    def _request(self, method, url, *,
                 params=None,
                 data=None,
                 json=None,
                 headers=None,
                 skip_auto_headers=None,
                 auth=None,
                 allow_redirects=True,
                 max_redirects=10,
                 encoding=None,
                 compress=None,
                 chunked=None,
                 expect100=False,
                 read_until_eof=True,
                 proxy=None,
                 proxy_auth=None,
                 timeout=DEFAULT_TIMEOUT):

        # NOTE: timeout clamps existing connect and read timeouts.  We cannot
        # set the default to None because we need to detect if the user wants
        # to use the existing timeouts by setting timeout to None.

        if encoding is not None:
            warnings.warn(
                "encoding parameter is not supported, "
                "please use FormData(charset='utf-8') instead",
                DeprecationWarning)

        if self.closed:
            raise RuntimeError('Session is closed')

        if data is not None and json is not None:
            raise ValueError(
                'data and json parameters can not be used at the same time')
        elif json is not None:
            data = payload.JsonPayload(json, dumps=self._json_serialize)

        if not isinstance(chunked, bool) and chunked is not None:
            warnings.warn(
                'Chunk size is deprecated #1615', DeprecationWarning)

        redirects = 0
        history = []
        version = self._version

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

        # timeout is cumulative for all request operations
        # (request, redirects, responses, data consuming)
        tm = TimeoutHandle(
            self._loop, timeout if timeout is not None else self._read_timeout)
        handle = tm.start()

        timer = tm.timer()
        try:
            with timer:
                while True:
                    url = URL(url).with_fragment(None)
                    cookies = self._cookie_jar.filter_cookies(url)

                    req = self._request_class(
                        method, url, params=params, headers=headers,
                        skip_auto_headers=skip_headers, data=data,
                        cookies=cookies, auth=auth, version=version,
                        compress=compress, chunked=chunked,
                        expect100=expect100, loop=self._loop,
                        response_class=self._response_class,
                        proxy=proxy, proxy_auth=proxy_auth, timer=timer)

                    # connection timeout
                    try:
                        with CeilTimeout(self._conn_timeout, loop=self._loop):
                            conn = yield from self._connector.connect(req)
                    except asyncio.TimeoutError as exc:
                        raise ServerTimeoutError(
                            'Connection timeout '
                            'to host {0}'.format(url)) from exc

                    conn.writer.set_tcp_nodelay(True)
                    try:
                        resp = req.send(conn)
                        try:
                            yield from resp.start(conn, read_until_eof)
                        except:
                            resp.close()
                            conn.close()
                            raise
                    except ClientError:
                        raise
                    except http.HttpProcessingError as exc:
                        raise ClientResponseError(
                            code=exc.code,
                            message=exc.message, headers=exc.headers) from exc
                    except OSError as exc:
                        raise ClientOSError(*exc.args) from exc

                    self._cookie_jar.update_cookies(resp.cookies, resp.url)

                    # redirects
                    if resp.status in (301, 302, 303, 307) and allow_redirects:
                        redirects += 1
                        history.append(resp)
                        if max_redirects and redirects >= max_redirects:
                            resp.close()
                            break
                        else:
                            resp.release()

                        # For 301 and 302, mimic IE, now changed in RFC
                        # https://github.com/kennethreitz/requests/pull/269
                        if (resp.status == 303 and
                                resp.method != hdrs.METH_HEAD) \
                                or (resp.status in (301, 302) and
                                    resp.method == hdrs.METH_POST):
                            method = hdrs.METH_GET
                            data = None
                            if headers.get(hdrs.CONTENT_LENGTH):
                                headers.pop(hdrs.CONTENT_LENGTH)

                        r_url = (resp.headers.get(hdrs.LOCATION) or
                                 resp.headers.get(hdrs.URI))
                        if r_url is None:
                            raise RuntimeError(
                                "{0.method} {0.url} returns "
                                "a redirect [{0.status}] status "
                                "but response lacks a Location "
                                "or URI HTTP header".format(resp))
                        r_url = URL(r_url)

                        scheme = r_url.scheme
                        if scheme not in ('http', 'https', ''):
                            resp.close()
                            raise ValueError(
                                'Can redirect only to http or https')
                        elif not scheme:
                            r_url = url.join(r_url)

                        url = r_url
                        params = None
                        resp.release()
                        continue

                    break

            # check response status
            if self._raise_for_status:
                resp.raise_for_status()

            # register connection
            if handle is not None:
                if resp.connection is not None:
                    resp.connection.add_callback(handle.cancel)
                else:
                    handle.cancel()

            resp._history = tuple(history)
            return resp

        except:
            # cleanup timer
            tm.close()
            if handle:
                handle.cancel()
                handle = None

            raise
