    def options(self, parser, env=os.environ):
        env_opt = 'PERFORM_GC'
        parser.add_option('--perform-gc', action='store_true',
                          dest='performGC', default=env.get(env_opt, False),
                          help='Call gc.collect() after each test')
