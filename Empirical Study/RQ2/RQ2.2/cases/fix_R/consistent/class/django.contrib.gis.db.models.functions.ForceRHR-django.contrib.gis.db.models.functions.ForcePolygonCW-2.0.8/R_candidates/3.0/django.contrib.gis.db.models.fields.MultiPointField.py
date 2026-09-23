class MultiPointField(GeometryField):
    geom_type = 'MULTIPOINT'
    geom_class = MultiPoint
    form_class = forms.MultiPointField
    description = _("Multi-point")
