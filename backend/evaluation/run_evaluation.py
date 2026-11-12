
import csv
from pathlib import Path
import argparse

from backend.app.services.indicator_service import (
    extract_sensitive_information_requests,
    extract_threat_indicators,
    extract_urgency_indicators,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_DATASET = (
    PROJECT_ROOT / "backend" / "data" / "evaluation" / "messages.csv"
)

INDICATOR_FUNCTIONS = {
    "urgency": extract_urgency_indicators,
    "threat": extract_threat_indicators,
    "sensitive_information_request": (
        extract_sensitive_information_requests
    ),
}


def evaluate_message(message: str) -> set[str]:
    detected = set()

    for category, extraction_function in INDICATOR_FUNCTIONS.items():
        results = extraction_function(message)

        if results:
            detected.add(category)

    return detected


def calculate_metrics(expected: set[str], actual: set[str]):
    true_positive = len(expected & actual)
    false_positive = len(actual - expected)
    false_negative = len(expected - actual)

    precision = (
        true_positive / (true_positive + false_positive)
        if true_positive + false_positive else 0
    )

    recall = (
        true_positive / (true_positive + false_negative)
        if true_positive + false_negative else 0
    )

    f1_score = (
        2 * precision * recall / (precision + recall)
        if precision + recall else 0
    )

    return {
        "TP": true_positive,
        "FP": false_positive,
        "FN": false_negative,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
    }

def get_dataset_path():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset",
        type=str,
        default=str(DEFAULT_DATASET),
    )
    args = parser.parse_args()

    return Path(args.dataset)

def main():
    results = []
    indicator_expected = {
        category: set() for category in INDICATOR_FUNCTIONS
    }
    indicator_actual = {
        category: set() for category in INDICATOR_FUNCTIONS
    }

    dataset_path = get_dataset_path()

    with open(dataset_path, encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            message_id = row["message_id"]
            message = row["message"]

            expected = set(
                row["expected_indicators"].split("|")
            ) - {""}

            actual = evaluate_message(message)

            for category in INDICATOR_FUNCTIONS:
                if category in expected:
                    indicator_expected[category].add(message_id)

                if category in actual:
                    indicator_actual[category].add(message_id)

            expected_label = row["expected_label"]
            actual_label = (
                "suspicious" if actual else "benign"
            )

            results.append({
                "message_id": message_id,
                "expected_label": expected_label,
                "actual_label": actual_label,
                "expected_indicators": "|".join(sorted(expected)),
                "actual_indicators": "|".join(sorted(actual)),
                "correct": expected == actual,
            })

    print("\nMESSAGE-LEVEL RESULTS")
    print("=" * 65)

    for result in results:
        status = "PASS" if result["correct"] else "FAIL"

        print(
            f"{result['message_id']} | {status} | "
            f"Expected: {result['expected_indicators']} | "
            f"Actual: {result['actual_indicators']}"
        )

    print("\nINDICATOR-LEVEL METRICS")
    print("=" * 65)

    for category in INDICATOR_FUNCTIONS:
        metrics = calculate_metrics(
            indicator_expected[category],
            indicator_actual[category],
        )

        print(f"\n{category}")
        for name, value in metrics.items():
            if isinstance(value, float):
                print(f"{name}: {value:.3f}")
            else:
                print(f"{name}: {value}")

    correct_messages = sum(
        result["correct"] for result in results
    )

    print("\nOVERALL INDICATOR MATCH")
    print("=" * 65)
    print(f"Correct messages: {correct_messages}/{len(results)}")
    print(
        f"Exact-match rate: "
        f"{correct_messages / len(results):.2%}"
    )

    output_path = PROJECT_ROOT / "evaluation_results.csv"

    with open(output_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys(),
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"\nDetailed results saved to: {output_path}")


if __name__ == "__main__":
    main()
