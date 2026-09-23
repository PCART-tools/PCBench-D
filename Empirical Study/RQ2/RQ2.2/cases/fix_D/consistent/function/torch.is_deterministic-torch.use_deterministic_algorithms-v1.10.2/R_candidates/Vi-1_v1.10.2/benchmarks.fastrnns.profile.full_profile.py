def full_profile(rnns, **args):
    profile_args = []
    for k, v in args.items():
        profile_args.append('--{}={}'.format(k, v))
    profile_args.append('--rnns {}'.format(' '.join(rnns)))
    profile_args.append('--internal_run')

    outpath = nvprof_output_filename(rnns, **args)

    cmd = '{} -m fastrnns.profile {}'.format(
        sys.executable, ' '.join(profile_args))
    rc, stdout, stderr = nvprof(cmd, outpath)
    if rc != 0:
        raise RuntimeError('stderr: {}\nstdout: {}'.format(stderr, stdout))
