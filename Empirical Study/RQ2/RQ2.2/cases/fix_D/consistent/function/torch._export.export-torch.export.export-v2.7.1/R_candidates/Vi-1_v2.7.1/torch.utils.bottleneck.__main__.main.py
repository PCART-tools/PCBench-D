def main():
    args = parse_args()

    # Customizable constants.
    scriptfile = args.scriptfile
    scriptargs = [] if args.args is None else args.args
    scriptargs.insert(0, scriptfile)
    cprofile_sortby = 'tottime'
    cprofile_topk = 15
    autograd_prof_sortby = 'cpu_time_total'
    autograd_prof_topk = 15

    redirect_argv(scriptargs)

    sys.path.insert(0, os.path.dirname(scriptfile))
    with open(scriptfile, 'rb') as stream:
        code = compile(stream.read(), scriptfile, 'exec')
    globs = {
        '__file__': scriptfile,
        '__name__': '__main__',
        '__package__': None,
        '__cached__': None,
    }

    print(descript)

    env_summary = run_env_analysis()

    if torch.cuda.is_available():
        torch.cuda.init()
    cprofile_prof = run_cprofile(code, globs)
    autograd_prof_cpu, autograd_prof_cuda = run_autograd_prof(code, globs)

    print(env_summary)
    print_cprofile_summary(cprofile_prof, cprofile_sortby, cprofile_topk)

    if not torch.cuda.is_available():
        print_autograd_prof_summary(autograd_prof_cpu, 'CPU', autograd_prof_sortby, autograd_prof_topk)
        return

    # Print both the result of the CPU-mode and CUDA-mode autograd profilers
    # if their execution times are very different.
    cuda_prof_exec_time = cpu_time_total(autograd_prof_cuda)
    if len(autograd_prof_cpu.function_events) > 0:
        cpu_prof_exec_time = cpu_time_total(autograd_prof_cpu)
        pct_diff = (cuda_prof_exec_time - cpu_prof_exec_time) / cuda_prof_exec_time
        if abs(pct_diff) > 0.05:
            print_autograd_prof_summary(autograd_prof_cpu, 'CPU', autograd_prof_sortby, autograd_prof_topk)

    print_autograd_prof_summary(autograd_prof_cuda, 'CUDA', autograd_prof_sortby, autograd_prof_topk)
