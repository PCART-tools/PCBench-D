class ServerThread(threading.Thread):
    def run(self):
        tornado.ioloop.IOLoop.instance().start()
