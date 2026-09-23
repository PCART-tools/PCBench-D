    @classmethod
    def tearDownClass(cls):
        _do_cleanup(cls.original_units_registry,
                    cls.original_settings)
