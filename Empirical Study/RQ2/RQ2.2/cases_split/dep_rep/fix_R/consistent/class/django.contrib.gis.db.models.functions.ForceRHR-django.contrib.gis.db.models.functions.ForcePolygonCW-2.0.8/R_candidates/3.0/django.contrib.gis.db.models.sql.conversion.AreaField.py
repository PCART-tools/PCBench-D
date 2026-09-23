class AreaField(models.FloatField):
    "Wrapper for Area values."
    def __init__(self, geo_field):
        super().__init__()
        self.geo_field = geo_field

    def get_prep_value(self, value):
        if not isinstance(value, Area):
            raise ValueError('AreaField only accepts Area measurement objects.')
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return
        area_att = connection.ops.get_area_att_for_field(self.geo_field)
        return getattr(value, area_att) if area_att else value

    def from_db_value(self, value, expression, connection):
        if value is None:
            return
        # If the database returns a Decimal, convert it to a float as expected
        # by the Python geometric objects.
        if isinstance(value, Decimal):
            value = float(value)
        # If the units are known, convert value into area measure.
        area_att = connection.ops.get_area_att_for_field(self.geo_field)
        return Area(**{area_att: value}) if area_att else value

    def get_internal_type(self):
        return 'AreaField'
