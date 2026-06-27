import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data
    evidence, labels = load_data(sys.argv[1])

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model
    model = train_model(X_train, y_train)

    # Predict
    predictions = model.predict(X_test)

    # Evaluate
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load CSV and return evidence and labels.
    """

    months = {
        "Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3,
        "May": 4, "Jun": 5, "Jul": 6, "Aug": 7,
        "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11
    }

    evidence = []
    labels = []

    with open(filename, newline="") as f:
        reader = csv.reader(f)
        next(reader)  # skip header

        for row in reader:

            evidence.append([
                int(row[0]),
                float(row[1]),
                int(row[2]),
                float(row[3]),
                int(row[4]),
                float(row[5]),
                float(row[6]),
                float(row[7]),
                float(row[8]),
                float(row[9]),
                months[row[10]],
                int(row[11]),
                int(row[12]),
                int(row[13]),
                int(row[14]),
                1 if row[15] == "Returning_Visitor" else 0,
                1 if row[16] == "TRUE" else 0
            ])

            labels.append(1 if row[17] == "TRUE" else 0)

    return evidence, labels


def train_model(evidence, labels):
    """
    Train kNN model (k=1).
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Compute sensitivity and specificity.
    """

    actual_positive = 0
    correct_positive = 0
    actual_negative = 0
    correct_negative = 0

    for actual, predicted in zip(labels, predictions):

        if actual == 1:
            actual_positive += 1
            if predicted == 1:
                correct_positive += 1
        else:
            actual_negative += 1
            if predicted == 0:
                correct_negative += 1

    sensitivity = (
        correct_positive / actual_positive if actual_positive else 0
    )

    specificity = (
        correct_negative / actual_negative if actual_negative else 0
    )

    return sensitivity, specificity


if __name__ == "__main__":
    main()