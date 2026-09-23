class GeometryDistance(GeoFunc):
    output_field = FloatField()
    arity = 2
    function = ''
    arg_joiner = ' <-> '
    geom_param_pos = (0, 1)
