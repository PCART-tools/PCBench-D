def emit_assignments(o, env):
    for i, r in enumerate(o['returns']):
        t = RETURN_MAP[r['type'] if not value_is_tensor_type(r) else 'at::Tensor']
        assignment = CT(t).substitute(env, offset=i, output=get_output(o, i))
        check_size_assignment = ASSIGN_CHECK_SIZE_TEMPLATE.substitute(env, offset=i, assignment=assignment)

        env['assignments'].append(check_size_assignment)
