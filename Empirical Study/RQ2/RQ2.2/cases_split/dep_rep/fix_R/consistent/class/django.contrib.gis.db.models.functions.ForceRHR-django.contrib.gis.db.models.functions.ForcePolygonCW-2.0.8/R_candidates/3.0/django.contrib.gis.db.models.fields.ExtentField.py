class ExtentField(Field):
    "Used as a return value from an extent aggregate"

    description = _("Extent Aggregate Field")

    def get_internal_type(self):
        return "ExtentField"

    def select_format(self, compiler, sql, params):
        select = compiler.connection.ops.select_extent
        return select % sql if select else sql, params
