    def create_wsgi_environ(self, message, payload):
        uri_parts = urlsplit(message.path)

        environ = {
            'wsgi.input': payload,
            'wsgi.errors': sys.stderr,
            'wsgi.version': (1, 0),
            'wsgi.async': True,
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
            'wsgi.file_wrapper': FileWrapper,
            'SERVER_SOFTWARE': aiohttp.HttpMessage.SERVER_SOFTWARE,
            'REQUEST_METHOD': message.method,
            'QUERY_STRING': uri_parts.query or '',
            'RAW_URI': message.path,
            'SERVER_PROTOCOL': 'HTTP/%s.%s' % message.version
        }

        script_name = self.SCRIPT_NAME

        for hdr_name, hdr_value in message.headers.items():
            hdr_name = hdr_name.upper()
            if hdr_name == 'SCRIPT_NAME':
                script_name = hdr_value
            elif hdr_name == 'CONTENT-TYPE':
                environ['CONTENT_TYPE'] = hdr_value
                continue
            elif hdr_name == 'CONTENT-LENGTH':
                environ['CONTENT_LENGTH'] = hdr_value
                continue

            key = 'HTTP_%s' % hdr_name.replace('-', '_')
            if key in environ:
                hdr_value = '%s,%s' % (environ[key], hdr_value)

            environ[key] = hdr_value

        url_scheme = environ.get('HTTP_X_FORWARDED_PROTO')
        if url_scheme is None:
            url_scheme = 'https' if self.is_ssl else 'http'
        environ['wsgi.url_scheme'] = url_scheme

        # authors should be aware that REMOTE_HOST and REMOTE_ADDR
        # may not qualify the remote addr
        # also SERVER_PORT variable MUST be set to the TCP/IP port number on
        # which this request is received from the client.
        # http://www.ietf.org/rfc/rfc3875

        family = self.transport.get_extra_info('socket').family
        if family in (socket.AF_INET, socket.AF_INET6):
            peername = self.transport.get_extra_info('peername')
            environ['REMOTE_ADDR'] = peername[0]
            environ['REMOTE_PORT'] = str(peername[1])
            http_host = message.headers.get("HOST", None)
            if http_host:
                hostport = http_host.split(":")
                environ['SERVER_NAME'] = hostport[0]
                if len(hostport) > 1:
                    environ['SERVER_PORT'] = str(hostport[1])
                else:
                    environ['SERVER_PORT'] = '80'
            else:
                # SERVER_NAME should be set to value of Host header, but this
                # header is not required. In this case we shoud set it to local
                # address of socket
                sockname = self.transport.get_extra_info('sockname')
                environ['SERVER_NAME'] = sockname[0]
                environ['SERVER_PORT'] = str(sockname[1])
        else:
            # We are behind reverse proxy, so get all vars from headers
            for header in ('REMOTE_ADDR', 'REMOTE_PORT',
                           'SERVER_NAME', 'SERVER_PORT'):
                environ[header] = message.headers.get(header, '')

        path_info = uri_parts.path
        if script_name:
            path_info = path_info.split(script_name, 1)[-1]

        environ['PATH_INFO'] = path_info
        environ['SCRIPT_NAME'] = script_name

        environ['async.reader'] = self.reader
        environ['async.writer'] = self.writer

        return environ
