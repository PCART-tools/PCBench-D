    @classmethod
    def start(cls):
        import asyncio
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            pass
        else:
            cls.started = True

        if cls.started:
            return

        """
        IOLoop.running() was removed as of Tornado 2.4; see for example
        https://groups.google.com/forum/#!topic/python-tornado/QLMzkpQBGOY
        Thus there is no correct way to check if the loop has already been
        launched. We may end up with two concurrently running loops in that
        unlucky case with all the expected consequences.
        """
        ioloop = tornado.ioloop.IOLoop.instance()

        def shutdown():
            ioloop.stop()
            print("Server is stopped")
            sys.stdout.flush()
            cls.started = False

        @contextmanager
        def catch_sigint():
            old_handler = signal.signal(
                signal.SIGINT,
                lambda sig, frame: ioloop.add_callback_from_signal(shutdown))
            try:
                yield
            finally:
                signal.signal(signal.SIGINT, old_handler)

        # Set the flag to True *before* blocking on ioloop.start()
        cls.started = True

        print("Press Ctrl+C to stop WebAgg server")
        sys.stdout.flush()
        with catch_sigint():
            ioloop.start()
