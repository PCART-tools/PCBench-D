class LineStringField(GeometryField):
    geom_type = 'LINESTRING'
    geom_class = LineString
    form_class = forms.LineStringField
    description = _("Line string")
