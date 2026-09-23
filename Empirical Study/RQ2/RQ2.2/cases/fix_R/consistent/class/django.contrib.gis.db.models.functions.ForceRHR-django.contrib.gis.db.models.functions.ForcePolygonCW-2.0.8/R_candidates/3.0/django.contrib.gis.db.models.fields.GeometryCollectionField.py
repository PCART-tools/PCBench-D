class GeometryCollectionField(GeometryField):
    geom_type = 'GEOMETRYCOLLECTION'
    geom_class = GeometryCollection
    form_class = forms.GeometryCollectionField
    description = _("Geometry collection")
