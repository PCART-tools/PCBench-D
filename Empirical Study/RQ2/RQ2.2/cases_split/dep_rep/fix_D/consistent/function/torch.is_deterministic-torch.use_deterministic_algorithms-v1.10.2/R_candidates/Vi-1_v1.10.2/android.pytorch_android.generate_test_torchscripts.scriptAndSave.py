def scriptAndSave(module, fileName):
    print('-' * 80)
    script_module = torch.jit.script(module)
    print(script_module.graph)
    outputFileName = OUTPUT_DIR + fileName
    script_module.save(outputFileName)
    print("Saved to " + outputFileName)
    print('=' * 80)
