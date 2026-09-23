class MultiLineStringField(GeometryField):
    geom_type = 'MULTILINESTRING'
    geom_class = MultiLineString
    form_class = forms.MultiLineStringField
    description = _("Multi-line string")
