    def quote_value(self, value):
        # The backend "mostly works" without this function and there are use
        # cases for compiling Python without the sqlite3 libraries (e.g.
        # security hardening).
        try:
            import sqlite3
            value = sqlite3.adapt(value)
        except ImportError:
            pass
        except sqlite3.ProgrammingError:
            pass
        # Manual emulation of SQLite parameter quoting
        if isinstance(value, type(True)):
            return str(int(value))
        elif isinstance(value, (Decimal, float)):
            return str(value)
        elif isinstance(value, six.integer_types):
            return str(value)
        elif isinstance(value, six.string_types):
            return "'%s'" % six.text_type(value).replace("\'", "\'\'")
        elif value is None:
            return "NULL"
        elif isinstance(value, (bytes, bytearray, six.memoryview)):
            # Bytes are only allowed for BLOB fields, encoded as string
            # literals containing hexadecimal data and preceded by a single "X"
            # character:
            # value = b'\x01\x02' => value_hex = b'0102' => return X'0102'
            value = bytes(value)
            hex_encoder = codecs.getencoder('hex_codec')
            value_hex, _length = hex_encoder(value)
            # Use 'ascii' encoding for b'01' => '01', no need to use force_text here.
            return "X'%s'" % value_hex.decode('ascii')
        else:
            raise ValueError("Cannot quote parameter value %r of type %s" % (value, type(value)))
