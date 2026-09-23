def setUpLocalServerInThread():
    try:
        Handler = partial(FileLoggerSimpleHTTPRequestHandler, logfile=None)
        socketserver.TCPServer.allow_reuse_address = True

        server = socketserver.TCPServer(("", 0), Handler)
        server_addr = "{host}:{port}".format(host=server.server_address[0], port=server.server_address[1])
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.start()

        # Wait a bit for the server to come up
        time.sleep(3)

        return (server_thread, server_addr, server)
    except Exception:
        raise
