    def __init__(self, param, cursor, strings_only=False):
        # With raw SQL queries, datetimes can reach this function
        # without being converted by DateTimeField.get_db_prep_value.
        if settings.USE_TZ and (isinstance(param, datetime.datetime) and
                                not isinstance(param, Oracle_datetime)):
            if timezone.is_aware(param):
                warnings.warn(
                    "The Oracle database adapter received an aware datetime (%s), "
                    "probably from cursor.execute(). Update your code to pass a "
                    "naive datetime in the database connection's time zone (UTC by "
                    "default).", RemovedInDjango20Warning)
                param = param.astimezone(timezone.utc).replace(tzinfo=None)
            param = Oracle_datetime.from_datetime(param)

        string_size = 0
        # Oracle doesn't recognize True and False correctly in Python 3.
        # The conversion done below works both in 2 and 3.
        if param is True:
            param = 1
        elif param is False:
            param = 0
        if hasattr(param, 'bind_parameter'):
            self.force_bytes = param.bind_parameter(cursor)
        elif isinstance(param, (Database.Binary, datetime.timedelta)):
            self.force_bytes = param
        else:
            # To transmit to the database, we need Unicode if supported
            # To get size right, we must consider bytes.
            self.force_bytes = force_text(param, cursor.charset, strings_only)
            if isinstance(self.force_bytes, six.string_types):
                # We could optimize by only converting up to 4000 bytes here
                string_size = len(force_bytes(param, cursor.charset, strings_only))
        if hasattr(param, 'input_size'):
            # If parameter has `input_size` attribute, use that.
            self.input_size = param.input_size
        elif string_size > 4000:
            # Mark any string param greater than 4000 characters as a CLOB.
            self.input_size = Database.CLOB
        elif isinstance(param, decimal.Decimal):
            self.input_size = Database.NUMBER
        else:
            self.input_size = None
