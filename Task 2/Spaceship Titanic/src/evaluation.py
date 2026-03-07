from sklearn.metrics import accuracy_score, classification_report

class Evaluator:
    def evaluate(self, y_test, predictions):
        print("Accuracy:", accuracy_score(y_test, predictions))
        print("\nClassification Report:\n")
        print(classification_report(y_test, predictions))