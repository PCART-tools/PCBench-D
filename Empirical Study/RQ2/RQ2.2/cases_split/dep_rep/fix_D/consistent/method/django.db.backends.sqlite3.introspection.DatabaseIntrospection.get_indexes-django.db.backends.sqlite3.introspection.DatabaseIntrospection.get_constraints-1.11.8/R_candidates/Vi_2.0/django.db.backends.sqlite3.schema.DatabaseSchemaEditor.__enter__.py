    def __enter__(self):
        # Some SQLite schema alterations need foreign key constraints to be
        # disabled. Enforce it here for the duration of the transaction.
        self.connection.disable_constraint_checking()
        return super().__enter__()
