class _ClassificationModel(  # pylint: disable=abstract-method
    _SparkXGBModel, HasProbabilityCol, HasRawPredictionCol, HasContribPredictionCol
):
    """
    The model returned by :func:`xgboost.spark.SparkXGBClassifier.fit`

    .. Note:: This API is experimental.
    """

    def _out_schema(self) -> Tuple[bool, str]:
        schema = (
            f"{pred.raw_prediction} array<double>, {pred.prediction} double,"
            f" {pred.probability} array<double>"
        )
        if self._get_pred_contrib_col_name() is not None:
            # We will force setting strict_shape to True when predicting contribs,
            # So, it will also output 3-D shape result.
            schema = f"{schema}, {pred.pred_contrib} array<array<double>>"

        return False, schema

    def _get_predict_func(self) -> Callable:
        predict_params = self._gen_predict_params_dict()
        pred_contrib_col_name = self._get_pred_contrib_col_name()

        def transform_margin(margins: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
            if margins.ndim == 1:
                # binomial case
                classone_probs = expit(margins)
                classzero_probs = 1.0 - classone_probs
                raw_preds = np.vstack((-margins, margins)).transpose()
                class_probs = np.vstack((classzero_probs, classone_probs)).transpose()
            else:
                # multinomial case
                raw_preds = margins
                class_probs = softmax(raw_preds, axis=1)
            return raw_preds, class_probs

        def _predict(
            model: XGBModel, X: ArrayLike, base_margin: Optional[np.ndarray]
        ) -> Union[pd.DataFrame, pd.Series]:
            margins = model.predict(
                X,
                base_margin=base_margin,
                output_margin=True,
                validate_features=False,
                **predict_params,
            )
            raw_preds, class_probs = transform_margin(margins)

            # It seems that they use argmax of class probs,
            # not of margin to get the prediction (Note: scala implementation)
            preds = np.argmax(class_probs, axis=1)
            result: Dict[str, pd.Series] = {
                pred.raw_prediction: pd.Series(list(raw_preds)),
                pred.prediction: pd.Series(preds),
                pred.probability: pd.Series(list(class_probs)),
            }

            if pred_contrib_col_name is not None:
                contribs = pred_contribs(model, X, base_margin, strict_shape=True)
                result[pred.pred_contrib] = pd.Series(list(contribs.tolist()))

            return pd.DataFrame(data=result)

        return _predict

    def _post_transform(self, dataset: DataFrame, pred_col: Column) -> DataFrame:
        pred_struct_col = "_prediction_struct"
        dataset = dataset.withColumn(pred_struct_col, pred_col)

        raw_prediction_col_name = self.getOrDefault(self.rawPredictionCol)
        if raw_prediction_col_name:
            dataset = dataset.withColumn(
                raw_prediction_col_name,
                array_to_vector(getattr(col(pred_struct_col), pred.raw_prediction)),
            )

        prediction_col_name = self.getOrDefault(self.predictionCol)
        if prediction_col_name:
            dataset = dataset.withColumn(
                prediction_col_name, getattr(col(pred_struct_col), pred.prediction)
            )

        probability_col_name = self.getOrDefault(self.probabilityCol)
        if probability_col_name:
            dataset = dataset.withColumn(
                probability_col_name,
                array_to_vector(getattr(col(pred_struct_col), pred.probability)),
            )

        pred_contrib_col_name = self._get_pred_contrib_col_name()
        if pred_contrib_col_name is not None:
            dataset = dataset.withColumn(
                pred_contrib_col_name,
                getattr(col(pred_struct_col), pred.pred_contrib),
            )

        return dataset.drop(pred_struct_col)
