    def quote_value(self, value):
        if isinstance(value, (datetime.date, datetime.time, datetime.datetime)):
            return "'%s'" % value
        elif isinstance(value, six.string_types):
            return "'%s'" % six.text_type(value).replace("\'", "\'\'")
        elif isinstance(value, six.buffer_types):
            return "'%s'" % force_text(binascii.hexlify(value))
        elif isinstance(value, bool):
            return "1" if value else "0"
        else:
            return str(value)
