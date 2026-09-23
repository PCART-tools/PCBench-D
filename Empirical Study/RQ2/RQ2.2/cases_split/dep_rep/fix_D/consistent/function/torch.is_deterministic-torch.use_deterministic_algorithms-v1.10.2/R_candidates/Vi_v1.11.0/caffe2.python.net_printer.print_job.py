@Printer.register(Job)
def print_job(text, job):
    text(job.init_group, 'Job.current().init_group')
    text(job.epoch_group, 'Job.current().epoch_group')
    with text.context('Job.current().stop_conditions'):
        for out in job.stop_conditions:
            text.add(_print_task_output(out))
    text(job.download_group, 'Job.current().download_group')
    text(job.exit_group, 'Job.current().exit_group')
