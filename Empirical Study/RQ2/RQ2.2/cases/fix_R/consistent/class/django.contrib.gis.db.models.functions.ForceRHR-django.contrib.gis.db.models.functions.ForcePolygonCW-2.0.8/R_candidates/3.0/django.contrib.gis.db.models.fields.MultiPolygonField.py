class MultiPolygonField(GeometryField):
    geom_type = 'MULTIPOLYGON'
    geom_class = MultiPolygon
    form_class = forms.MultiPolygonField
    description = _("Multi polygon")
