    def quote_value(self, value):
        if isinstance(value, str):
            value = value.replace("%", "%%")
        adapted = psycopg2.extensions.adapt(value)
        if hasattr(adapted, "encoding"):
            adapted.encoding = "utf8"
        # getquoted() returns a quoted bytestring of the adapted value.
        return adapted.getquoted().decode()
