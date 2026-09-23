def _unique_generic(values, table_type, type_caster):
    values = type_caster(values)
    table = table_type(min(len(values), 1000000))
    uniques = table.unique(values)
    return type_caster(uniques)
