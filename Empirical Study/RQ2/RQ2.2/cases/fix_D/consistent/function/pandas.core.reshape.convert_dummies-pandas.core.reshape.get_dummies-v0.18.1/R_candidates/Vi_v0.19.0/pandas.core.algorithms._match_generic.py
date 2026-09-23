def _match_generic(values, index, table_type, type_caster):
    values = type_caster(values)
    index = type_caster(index)
    table = table_type(min(len(index), 1000000))
    table.map_locations(index)
    return table.lookup(values)
