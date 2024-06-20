import sys
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd


TEST_SIZE = 0.4

MONTHS = {
    "Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3, "May": 4, "June": 5,
    "Jul": 6, "Aug": 7, "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11
}

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    df = pd.read_csv(filename)
    
    df['Month'] = df['Month'].map(MONTHS)

    df['VisitorType'] = df['VisitorType'].apply(lambda x: 1 if x == 'Returning_Visitor' else 0)

    df['Weekend'] = df['Weekend'].apply(lambda x: 1 if x == True else 0)

    df['Revenue'] = df['Revenue'].apply(lambda x: 1 if x == True else 0)

    evidence = df.drop('Revenue', axis=1).values
    labels = df['Revenue'].values

    return evidence, labels


def train_model(evidence, labels):
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    true_positive = sum((labels == 1) & (predictions == 1))
    true_negative = sum((labels == 0) & (predictions == 0))
    false_negative = sum((labels == 1) & (predictions == 0))
    false_positive = sum((labels == 0) & (predictions == 1))

    sensitivity = true_positive / (true_positive + false_negative)
    specificity = true_negative / (true_negative + false_positive)

    return sensitivity, specificity


if __name__ == "__main__":
    main()
