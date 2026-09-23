@Analyzer.register(Job)
def analyze_job(analyzer, job):
    analyzer(job.init_group)
    analyzer(job.epoch_group)
