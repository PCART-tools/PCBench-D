def print_cprofile_summary(prof, sortby='tottime', topk=15):
    print(cprof_summary)
    cprofile_stats = pstats.Stats(prof).sort_stats(sortby)
    cprofile_stats.print_stats(topk)
