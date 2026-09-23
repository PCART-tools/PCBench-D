def progressBar(percentage):
    full = int(DOWNLOAD_COLUMNS * percentage / 100)
    bar = full * "#" + (DOWNLOAD_COLUMNS - full) * " "
    sys.stdout.write(u"\u001b[1000D[" + bar + "] " + str(percentage) + "%")
    sys.stdout.flush()
