@register_transformation_rule(Disj)
def generate_disj(constraint, counter):
    """
    Transform disjunctions
    """
    new = []
    for c in constraint.disjuncts:
        new_c, counter = transform_constraint(c, counter)
        new.append(new_c)
    return Disj(new), counter
