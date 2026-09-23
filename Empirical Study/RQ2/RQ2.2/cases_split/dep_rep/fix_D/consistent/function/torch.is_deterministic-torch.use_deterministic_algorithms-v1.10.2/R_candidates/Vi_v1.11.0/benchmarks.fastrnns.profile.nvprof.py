def nvprof(cmd, outpath):
    return system('nvprof -o {} {}'.format(outpath, cmd))
