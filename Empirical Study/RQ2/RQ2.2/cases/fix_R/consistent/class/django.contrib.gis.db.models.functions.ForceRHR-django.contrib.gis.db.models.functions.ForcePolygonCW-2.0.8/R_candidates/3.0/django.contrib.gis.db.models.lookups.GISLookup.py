class GISLookup(Lookup):
    sql_template = None
    transform_func = None
    distance = False
    band_rhs = None
    band_lhs = None

    def __init__(self, lhs, rhs):
        rhs, *self.rhs_params = rhs if isinstance(rhs, (list, tuple)) else [rhs]
        super().__init__(lhs, rhs)
        self.template_params = {}
        self.process_rhs_params()

    def process_rhs_params(self):
        if self.rhs_params:
            # Check if a band index was passed in the query argument.
            if len(self.rhs_params) == (2 if self.lookup_name == 'relate' else 1):
                self.process_band_indices()
            elif len(self.rhs_params) > 1:
                raise ValueError('Tuple too long for lookup %s.' % self.lookup_name)
        elif isinstance(self.lhs, RasterBandTransform):
            self.process_band_indices(only_lhs=True)

    def process_band_indices(self, only_lhs=False):
        """
        Extract the lhs band index from the band transform class and the rhs
        band index from the input tuple.
        """
        # PostGIS band indices are 1-based, so the band index needs to be
        # increased to be consistent with the GDALRaster band indices.
        if only_lhs:
            self.band_rhs = 1
            self.band_lhs = self.lhs.band_index + 1
            return

        if isinstance(self.lhs, RasterBandTransform):
            self.band_lhs = self.lhs.band_index + 1
        else:
            self.band_lhs = 1

        self.band_rhs, *self.rhs_params = self.rhs_params

    def get_db_prep_lookup(self, value, connection):
        # get_db_prep_lookup is called by process_rhs from super class
        return ('%s', [connection.ops.Adapter(value)])

    def process_rhs(self, compiler, connection):
        if isinstance(self.rhs, Query):
            # If rhs is some Query, don't touch it.
            return super().process_rhs(compiler, connection)
        if isinstance(self.rhs, Expression):
            self.rhs = self.rhs.resolve_expression(compiler.query)
        rhs, rhs_params = super().process_rhs(compiler, connection)
        placeholder = connection.ops.get_geom_placeholder(self.lhs.output_field, self.rhs, compiler)
        return placeholder % rhs, rhs_params

    def get_rhs_op(self, connection, rhs):
        # Unlike BuiltinLookup, the GIS get_rhs_op() implementation should return
        # an object (SpatialOperator) with an as_sql() method to allow for more
        # complex computations (where the lhs part can be mixed in).
        return connection.ops.gis_operators[self.lookup_name]

    def as_sql(self, compiler, connection):
        lhs_sql, sql_params = self.process_lhs(compiler, connection)
        rhs_sql, rhs_params = self.process_rhs(compiler, connection)
        sql_params.extend(rhs_params)

        template_params = {'lhs': lhs_sql, 'rhs': rhs_sql, 'value': '%s', **self.template_params}
        rhs_op = self.get_rhs_op(connection, rhs_sql)
        return rhs_op.as_sql(connection, self, template_params, sql_params)
