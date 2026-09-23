def main(argv):
    parser = argparse.ArgumentParser("The mint visualizer.")
    parser.add_argument(
        '-p',
        '--port',
        type=int,
        default=5000,
        help="The flask port to use."
    )
    parser.add_argument(
        '-r',
        '--root',
        type=str,
        default='.',
        help="The root folder to read files for visualization."
    )
    parser.add_argument(
        '--max_curves',
        type=int,
        default=5,
        help="The max number of curves to show in a dump tensor."
    )
    parser.add_argument(
        '--chart_height',
        type=int,
        default=300,
        help="The chart height for nvd3."
    )
    parser.add_argument(
        '-s',
        '--sample',
        type=int,
        default=-200,
        help="Sample every given number of data points. A negative "
        "number means the total points we will sample on the "
        "whole curve. Default 100 points."
    )
    global args
    args = parser.parse_args(argv)
    server = tornado.httpserver.HTTPServer(tornado.wsgi.WSGIContainer(app))
    server.listen(args.port)
    print("Tornado server starting on port {}.".format(args.port))
    tornado.ioloop.IOLoop.instance().start()
