    @staticmethod
    def is_in_memory_db(database_name):
        return database_name == ':memory:' or 'mode=memory' in database_name
