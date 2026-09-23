    def _start_transaction_under_autocommit(self):
        """
        Only required when autocommits_when_autocommit_is_off = True.
        """
        raise NotImplementedError(
            'subclasses of BaseDatabaseWrapper may require a '
            '_start_transaction_under_autocommit() method'
        )
