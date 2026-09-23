@_api.deprecated("3.5", alternative="psutil.virtual_memory")
def report_memory(i=0):  # argument may go away
    """Return the memory consumed by the process."""
    def call(command, os_name):
        try:
            return subprocess.check_output(command)
        except subprocess.CalledProcessError as err:
            raise NotImplementedError(
                "report_memory works on %s only if "
                "the '%s' program is found" % (os_name, command[0])
            ) from err

    pid = os.getpid()
    if sys.platform == 'sunos5':
        lines = call(['ps', '-p', '%d' % pid, '-o', 'osz'], 'Sun OS')
        mem = int(lines[-1].strip())
    elif sys.platform == 'linux':
        lines = call(['ps', '-p', '%d' % pid, '-o', 'rss,sz'], 'Linux')
        mem = int(lines[1].split()[1])
    elif sys.platform == 'darwin':
        lines = call(['ps', '-p', '%d' % pid, '-o', 'rss,vsz'], 'Mac OS')
        mem = int(lines[1].split()[0])
    elif sys.platform == 'win32':
        lines = call(["tasklist", "/nh", "/fi", "pid eq %d" % pid], 'Windows')
        mem = int(lines.strip().split()[-2].replace(',', ''))
    else:
        raise NotImplementedError(
            "We don't have a memory monitor for %s" % sys.platform)
    return mem
