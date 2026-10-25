from aidetect.ml_evaluation import cross_validate_model, evaluate_model, cross_validate_samples
from aidetect.ml_samples import DatasetSample


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



def test_cross_validate_model_returns_five_folds():
    X = [[float(i)] for i in range(20)]
    y = [0] * 10 + [1] * 10

    result = cross_validate_model(X, y, n_splits=5)

    assert len(result["folds"]) == 5

    assert 0.0 <= result["mean_accuracy"] <= 1.0
    assert 0.0 <= result["mean_precision"] <= 1.0
    assert 0.0 <= result["mean_recall"] <= 1.0
    assert 0.0 <= result["mean_f1"] <= 1.0



def test_cross_validate_samples_returns_all_samples():
    samples = [
        DatasetSample(
            id=f"sample_{i}",
            text="example text",
            label="human" if i < 10 else "ai",
            topic="test",
            source="manual" if i < 10 else "generated",
        )
        for i in range(20)
    ]

    X = [[float(i)] for i in range(20)]
    y = [0] * 10 + [1] * 10

    results = cross_validate_samples(samples, X, y, n_splits=5)

    assert len(results) == 20
    assert {result["id"] for result in results} == {
        sample.id for sample in samples
    }
    assert all(1 <= result["fold"] <= 5 for result in results)
