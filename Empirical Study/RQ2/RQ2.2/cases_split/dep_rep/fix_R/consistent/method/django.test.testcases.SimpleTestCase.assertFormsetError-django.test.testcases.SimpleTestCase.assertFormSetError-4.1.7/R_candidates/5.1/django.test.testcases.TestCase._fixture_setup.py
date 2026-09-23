    def _fixture_setup(self):
        if not self._databases_support_transactions():
            # If the backend does not support transactions, we should reload
            # class data before each test
            self.setUpTestData()
            return super()._fixture_setup()

        if self.reset_sequences:
            raise TypeError("reset_sequences cannot be used on TestCase instances")
        self.atomics = self._enter_atomics()
        if not self._databases_support_savepoints():
            if self.fixtures:
                for db_name in self._databases_names(include_mirrors=False):
                    call_command(
                        "loaddata",
                        *self.fixtures,
                        **{"verbosity": 0, "database": db_name},
                    )
            self.setUpTestData()
