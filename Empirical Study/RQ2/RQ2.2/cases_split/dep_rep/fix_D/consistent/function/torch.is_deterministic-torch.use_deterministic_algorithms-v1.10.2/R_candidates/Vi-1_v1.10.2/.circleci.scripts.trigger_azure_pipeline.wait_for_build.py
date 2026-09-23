def wait_for_build(_id):
    build_detail = get_build(_id)
    build_status = build_detail['status']

    while build_status == 'notStarted':
        print('Waiting for run to start: ' + str(_id))
        sys.stdout.flush()
        try:
            build_detail = get_build(_id)
            build_status = build_detail['status']
        except Exception as e:
            print("Error getting build")
            print(e)

        time.sleep(30)

    print("Bulid started: ", str(_id))

    handled_logs = set()
    while build_status == 'inProgress':
        try:
            print("Waiting for log: " + str(_id))
            logs = get_build_logs(_id)
        except Exception as e:
            print("Error fetching logs")
            print(e)
            time.sleep(30)
            continue

        for log in logs['value']:
            log_id = log['id']
            if log_id in handled_logs:
                continue
            handled_logs.add(log_id)
            print('Fetching log: \n' + log['url'])
            try:
                log_content = get_log_content(log['url'])
                print(log_content)
            except Exception as e:
                print("Error getting log content")
                print(e)
            sys.stdout.flush()
        build_detail = get_build(_id)
        build_status = build_detail['status']
        time.sleep(30)

    build_result = build_detail['result']

    print("Bulid status: " + build_status)
    print("Bulid result: " + build_result)

    return build_status, build_result
