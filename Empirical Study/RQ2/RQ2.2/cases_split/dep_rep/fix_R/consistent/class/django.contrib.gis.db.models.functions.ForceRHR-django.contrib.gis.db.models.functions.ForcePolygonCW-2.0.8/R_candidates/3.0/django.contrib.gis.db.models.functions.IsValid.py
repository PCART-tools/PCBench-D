@BaseSpatialField.register_lookup
class IsValid(OracleToleranceMixin, GeoFuncMixin, Transform):
    lookup_name = 'isvalid'
    output_field = BooleanField()

    def as_oracle(self, compiler, connection, **extra_context):
        sql, params = super().as_oracle(compiler, connection, **extra_context)
        return "CASE %s WHEN 'TRUE' THEN 1 ELSE 0 END" % sql, params
