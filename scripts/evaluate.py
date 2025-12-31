
from pathlib import Path
from aidetect.text.scorer import analyze_text


def load_texts(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]



def evaluate(texts: list[str], expected_label: str) -> dict:
    results = {
        "total": len(texts),
        "correct": 0,
        "incorrect": 0,
        "predicted_ai": 0,
    }

    for text in texts:
        result =analyze_text(text)

        if result.label == expected_label:
            results["correct"] += 1
        else:
            results["incorrect"] += 1

        if result.label == "ai":
            results["predicted_ai"] += 1

    return results



def main() -> None:
    base = Path("data/evaluation")

    human_texts = load_texts(base / "human.txt")
    ai_texts = load_texts(base / "ai.txt")

    human_eval = evaluate(human_texts, "human")
    ai_eval = evaluate(ai_texts, "ai")

    print("=== Evaluation results ===\n")

    print("Human texts:")
    print(human_eval, "\n")

    print("AI texts:")
    print(ai_eval, "\n")

    total = human_eval["total"] + ai_eval["total"]
    correct = human_eval["correct"] + ai_eval["correct"]

    accuracy = correct / total if total else 0.0

    print(f"Overall accuracy: {accuracy:.2}")



if __name__ == "__main__":
    main()
