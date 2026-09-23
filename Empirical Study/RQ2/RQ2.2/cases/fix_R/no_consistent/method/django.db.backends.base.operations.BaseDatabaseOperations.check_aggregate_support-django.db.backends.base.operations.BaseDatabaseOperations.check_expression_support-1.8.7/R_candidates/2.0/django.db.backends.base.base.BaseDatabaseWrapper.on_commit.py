    def on_commit(self, func):
        if self.in_atomic_block:
            # Transaction in progress; save for execution on commit.
            self.run_on_commit.append((set(self.savepoint_ids), func))
        elif not self.get_autocommit():
            raise TransactionManagementError('on_commit() cannot be used in manual transaction management')
        else:
            # No transaction in progress and in autocommit mode; execute
            # immediately.
            func()
