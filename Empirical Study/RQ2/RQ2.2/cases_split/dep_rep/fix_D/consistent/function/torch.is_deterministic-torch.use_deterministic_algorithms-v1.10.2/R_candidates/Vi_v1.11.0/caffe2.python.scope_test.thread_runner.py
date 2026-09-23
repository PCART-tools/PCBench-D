def thread_runner(idx, testobj):
    global SUCCESS_COUNT
    testobj.assertEquals(scope.CurrentNameScope(), "")
    testobj.assertEquals(scope.CurrentDeviceScope(), None)
    namescope = "namescope_{}".format(idx)
    dsc = core.DeviceOption(workspace.GpuDeviceType, idx)
    with scope.DeviceScope(dsc):
        with scope.NameScope(namescope):
            testobj.assertEquals(scope.CurrentNameScope(), namescope + "/")
            testobj.assertEquals(scope.CurrentDeviceScope(), dsc)

            time.sleep(0.01 + idx * 0.01)
            testobj.assertEquals(scope.CurrentNameScope(), namescope + "/")
            testobj.assertEquals(scope.CurrentDeviceScope(), dsc)

    testobj.assertEquals(scope.CurrentNameScope(), "")
    testobj.assertEquals(scope.CurrentDeviceScope(), None)
    SUCCESS_COUNT += 1
