@register_transformation_rule(Conj)
def generate_conj(constraint, counter):
    """
    Transform conjunctions
    """
    new = []
    for c in constraint.conjucts:
        new_c, counter = transform_constraint(c, counter)
        new.append(new_c)
    return Conj(new), counter
