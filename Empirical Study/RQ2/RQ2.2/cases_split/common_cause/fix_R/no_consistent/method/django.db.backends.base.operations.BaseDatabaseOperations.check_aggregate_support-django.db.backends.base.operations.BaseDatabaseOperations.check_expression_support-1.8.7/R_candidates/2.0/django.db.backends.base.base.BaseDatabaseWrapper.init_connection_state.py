    def init_connection_state(self):
        """Initialize the database connection settings."""
        raise NotImplementedError('subclasses of BaseDatabaseWrapper may require an init_connection_state() method')
