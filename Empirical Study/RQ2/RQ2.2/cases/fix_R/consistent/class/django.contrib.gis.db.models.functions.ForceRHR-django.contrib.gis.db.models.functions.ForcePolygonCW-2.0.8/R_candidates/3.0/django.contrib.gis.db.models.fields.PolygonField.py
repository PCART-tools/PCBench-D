class PolygonField(GeometryField):
    geom_type = 'POLYGON'
    geom_class = Polygon
    form_class = forms.PolygonField
    description = _("Polygon")
