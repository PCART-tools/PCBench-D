    def quote_value(self, value):
        if isinstance(value, (datetime.date, datetime.time, datetime.datetime)):
            return "'%s'" % value
        elif isinstance(value, str):
            return "'%s'" % value.replace("\'", "\'\'")
        elif isinstance(value, (bytes, bytearray, memoryview)):
            return "'%s'" % force_text(binascii.hexlify(value))
        elif isinstance(value, bool):
            return "1" if value else "0"
        else:
            return str(value)
