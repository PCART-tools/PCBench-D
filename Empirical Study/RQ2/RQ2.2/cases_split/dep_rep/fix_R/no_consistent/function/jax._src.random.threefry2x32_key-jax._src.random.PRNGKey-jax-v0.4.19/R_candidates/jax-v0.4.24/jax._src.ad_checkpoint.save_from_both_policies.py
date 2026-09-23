def save_from_both_policies(policy_1, policy_2):

  def policy(prim, *args, **params):
    return policy_1(prim, *args, **params) or policy_2(prim, *args, **params)

  return policy
