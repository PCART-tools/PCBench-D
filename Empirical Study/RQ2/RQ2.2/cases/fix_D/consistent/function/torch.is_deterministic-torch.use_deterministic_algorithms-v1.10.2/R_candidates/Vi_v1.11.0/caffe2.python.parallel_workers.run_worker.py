def run_worker(coordinator, worker):
    while coordinator.is_active():
        worker.start()
        try:
            worker.run()
        except Exception as e:
            worker.handle_exception(e)
        finally:
            worker.finish()
