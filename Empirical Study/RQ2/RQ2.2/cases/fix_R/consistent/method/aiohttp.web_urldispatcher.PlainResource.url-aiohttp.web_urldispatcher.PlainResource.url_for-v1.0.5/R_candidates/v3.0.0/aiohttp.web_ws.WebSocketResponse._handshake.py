    def _handshake(self, request):
        headers = request.headers
        if request.method != hdrs.METH_GET:
            raise HTTPMethodNotAllowed(request.method, [hdrs.METH_GET])
        if 'websocket' != headers.get(hdrs.UPGRADE, '').lower().strip():
            raise HTTPBadRequest(
                text=('No WebSocket UPGRADE hdr: {}\n Can '
                      '"Upgrade" only to "WebSocket".')
                .format(headers.get(hdrs.UPGRADE)))

        if 'upgrade' not in headers.get(hdrs.CONNECTION, '').lower():
            raise HTTPBadRequest(
                text='No CONNECTION upgrade hdr: {}'.format(
                    headers.get(hdrs.CONNECTION)))

        # find common sub-protocol between client and server
        protocol = None
        if hdrs.SEC_WEBSOCKET_PROTOCOL in headers:
            req_protocols = [str(proto.strip()) for proto in
                             headers[hdrs.SEC_WEBSOCKET_PROTOCOL].split(',')]

            for proto in req_protocols:
                if proto in self._protocols:
                    protocol = proto
                    break
            else:
                # No overlap found: Return no protocol as per spec
                ws_logger.warning(
                    'Client protocols %r don’t overlap server-known ones %r',
                    req_protocols, self._protocols)

        # check supported version
        version = headers.get(hdrs.SEC_WEBSOCKET_VERSION, '')
        if version not in ('13', '8', '7'):
            raise HTTPBadRequest(
                text='Unsupported version: {}'.format(version))

        # check client handshake for validity
        key = headers.get(hdrs.SEC_WEBSOCKET_KEY)
        try:
            if not key or len(base64.b64decode(key)) != 16:
                raise HTTPBadRequest(
                    text='Handshake error: {!r}'.format(key))
        except binascii.Error:
            raise HTTPBadRequest(
                text='Handshake error: {!r}'.format(key)) from None

        accept_val = base64.b64encode(
            hashlib.sha1(key.encode() + WS_KEY).digest()).decode()
        response_headers = CIMultiDict({hdrs.UPGRADE: 'websocket',
                                        hdrs.CONNECTION: 'upgrade',
                                        hdrs.TRANSFER_ENCODING: 'chunked',
                                        hdrs.SEC_WEBSOCKET_ACCEPT: accept_val})

        notakeover = False
        compress = self._compress
        if compress:
            extensions = headers.get(hdrs.SEC_WEBSOCKET_EXTENSIONS)
            # Server side always get return with no exception.
            # If something happened, just drop compress extension
            compress, notakeover = ws_ext_parse(extensions, isserver=True)
            if compress:
                enabledext = ws_ext_gen(compress=compress, isserver=True,
                                        server_notakeover=notakeover)
                response_headers[hdrs.SEC_WEBSOCKET_EXTENSIONS] = enabledext

        if protocol:
            response_headers[hdrs.SEC_WEBSOCKET_PROTOCOL] = protocol
        return (response_headers, protocol, compress, notakeover)
