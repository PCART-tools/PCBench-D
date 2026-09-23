def writeln(fh, line):
    # every line of a file included with \\input must be terminated with %
    # if not, latex will create additional vertical spaces for some reason
    fh.write(line)
    fh.write("%\n")
