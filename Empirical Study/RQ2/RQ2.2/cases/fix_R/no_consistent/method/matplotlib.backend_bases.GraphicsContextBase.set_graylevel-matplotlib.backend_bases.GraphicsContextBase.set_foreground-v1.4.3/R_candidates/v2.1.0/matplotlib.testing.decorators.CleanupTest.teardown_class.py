    @classmethod
    def teardown_class(cls):
        _do_cleanup(cls.original_units_registry,
                    cls.original_settings)
