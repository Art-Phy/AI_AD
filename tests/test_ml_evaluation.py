from aidetect.ml_evaluation import evaluate_model



class DummyModel:
    def __init__(self, predictions):
        self.predictions = predictions


    def predict(self, X):
        return self.predictions



def test_evaluate_model_perfect_predictions():
    X_test = [[1.0], [2.0], [3.0], [4.0]]
    y_test = [0, 0, 1, 1]

    model = DummyModel([0, 0, 1, 1])

    result = evaluate_model(model, X_test, y_test)

    assert result["accuracy"] == 1.0
    assert result["precision"] == 1.0
    assert result["recall"] == 1.0
    assert result["f1"] == 1.0
    assert result["confusion_matrix"] == [[2, 0], [0, 2]]
    assert result["predictions"] == [0, 0, 1, 1]



def test_evaluate_model_with_errors():
    X_test = [[1.0], [2.0], [3.0], [4.0]]
    y_test = [0, 0, 1, 1]

    model = DummyModel([0, 1, 0, 1])

    result = evaluate_model(model, X_test, y_test)

    assert result["accuracy"] == 0.5
    assert result["precision"] == 0.5
    assert result["recall"] == 0.5
    assert result["f1"] == 0.5
    assert result["confusion_matrix"] == [[1, 1], [1, 1]]
