def test_nested_child_body(i, ready_queue, nested_child_sleep):
    ready_queue.put(None)
    time.sleep(nested_child_sleep)
