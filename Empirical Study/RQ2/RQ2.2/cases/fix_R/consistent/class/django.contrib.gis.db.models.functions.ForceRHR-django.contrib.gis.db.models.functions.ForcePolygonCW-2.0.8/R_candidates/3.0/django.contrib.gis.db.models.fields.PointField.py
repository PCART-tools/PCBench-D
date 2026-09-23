class PointField(GeometryField):
    geom_type = 'POINT'
    geom_class = Point
    form_class = forms.PointField
    description = _("Point")
