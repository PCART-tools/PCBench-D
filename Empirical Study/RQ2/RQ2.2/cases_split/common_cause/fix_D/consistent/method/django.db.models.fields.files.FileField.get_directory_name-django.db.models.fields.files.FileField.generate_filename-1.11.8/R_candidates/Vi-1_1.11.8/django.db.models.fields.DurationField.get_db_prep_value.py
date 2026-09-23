    def get_db_prep_value(self, value, connection, prepared=False):
        if connection.features.has_native_duration_field:
            return value
        if value is None:
            return None
        # Discard any fractional microseconds due to floating point arithmetic.
        return int(round(value.total_seconds() * 1000000))
