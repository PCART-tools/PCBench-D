    def quote_value(self, value):
        return psycopg2.extensions.adapt(value)
