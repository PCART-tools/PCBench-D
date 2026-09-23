class BoundingCircle(OracleToleranceMixin, GeoFunc):
    def __init__(self, expression, num_seg=48, **extra):
        super().__init__(expression, num_seg, **extra)

    def as_oracle(self, compiler, connection, **extra_context):
        clone = self.copy()
        clone.set_source_expressions([self.get_source_expressions()[0]])
        return super(BoundingCircle, clone).as_oracle(compiler, connection, **extra_context)
