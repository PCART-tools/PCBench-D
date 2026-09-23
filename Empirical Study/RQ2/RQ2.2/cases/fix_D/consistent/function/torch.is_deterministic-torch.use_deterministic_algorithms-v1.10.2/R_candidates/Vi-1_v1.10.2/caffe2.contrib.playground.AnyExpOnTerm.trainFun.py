def trainFun():
    def simpleTrainFun(opts):
        trainerClass = AnyExp.createTrainerClass(opts)
        trainerClass = AnyExp.overrideAdditionalMethods(trainerClass, opts)
        trainer = trainerClass(opts)
        return trainer.buildModelAndTrain(opts)
    return simpleTrainFun
