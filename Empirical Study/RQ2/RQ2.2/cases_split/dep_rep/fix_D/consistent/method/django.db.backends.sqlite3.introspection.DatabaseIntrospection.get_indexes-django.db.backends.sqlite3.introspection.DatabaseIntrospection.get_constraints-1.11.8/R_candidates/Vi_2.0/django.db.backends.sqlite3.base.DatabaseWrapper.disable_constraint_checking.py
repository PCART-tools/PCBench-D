    def disable_constraint_checking(self):
        if self.in_atomic_block:
            # sqlite3 cannot disable constraint checking inside a transaction.
            return False
        self.cursor().execute('PRAGMA foreign_keys = OFF')
        return True
