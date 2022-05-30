import random

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from classifier import DecisionTree
import pandas as pd
from typing import List, Any, Callable

from math import log


class AdaBoost:
    def __init__(self, n_classifier: int = 5, seed: int = 42):
        random.seed(42)

        self.n_classifier: int = n_classifier

        # Function fit will later populate these variables
        self.target_attribute: str = None
        self.classes: List[Any] = []
        self.weights: List[List[float]] = []
        self.betas: List[float] = []
        self.classifiers: List[DecisionTree] = []

    def fit(self, dataset: pd.DataFrame, target_attribute: str):
        self.target_attribute = target_attribute
        self._initialize_weights(dataset=dataset)
        y = dataset[target_attribute].tolist()
        self.classes = dataset[target_attribute].unique().tolist()
        n_tuples = dataset.shape[0]

        while True:
            # Stop while-loop when there are enough classifiers
            if len(self.classifiers) == self.n_classifier:
                break

            # Normalize weights
            weights_normalized = self._normalize_weights(weights=self.weights[-1])

            current_dataset = dataset.sample(
                n=n_tuples,
                weights=weights_normalized,
                replace=True,
                random_state=42,
                axis=0,
            )

            # Call weak_learn to obtain the current trained classifier
            current_classifier = self._weak_learn(dataset=current_dataset)

            # Obtain prediction from current classifier
            current_predictions = current_classifier.predict(dataset=current_dataset)

            # Calculate error of current classifier
            missclassification_errors = [
                self._missclassification_error(true_value, predicted)
                for true_value, predicted in zip(
                    current_dataset[target_attribute],
                    current_predictions,
                )
            ]
            current_error = sum(
                [
                    w_i * err_i
                    for w_i, err_i in zip(weights_normalized, missclassification_errors)
                ]
            )

            # If error is greater than 0.5 abort loop and start again
            if current_error > 0.5:
                continue

            # Calculate beta
            current_beta = current_error / (1 - current_error)

            # Append current beta to the list of betas
            self.betas.append(current_beta)

            # Calculate and normalize weights for next iteration
            new_weights = self._calculate_new_weights(
                weights=self.weights[-1],
                beta=current_beta,
                error=missclassification_errors,
            )

            # Append current weights to the list of weights
            self.weights.append(new_weights)

            # Append current weak classifier to the list of classifiers
            self.classifiers.append(current_classifier)

    def _initialize_weights(self, dataset: pd.DataFrame):
        """Initialize weights if they have not been initialized before.
        Formula: weights = 1 / number of tuples in data"""
        if not self.weights:
            n_tuples = dataset.shape[0]
            self.weights.append([1 / n_tuples for _ in range(n_tuples)])

    def _weak_learn(self, dataset: pd.DataFrame):
        # Instantiate weak classifier
        classifier = DecisionTree()

        # Train weak classifier
        classifier.fit(dataset=dataset, target_attribute=self.target_attribute)
        return classifier

    @staticmethod
    def _missclassification_error(true: List[float], predicted: List[float]):
        """Calculate the missclassification error.
        Returns 1 if missclassified (true != predicted), 0 if correct (true == predicted)."""
        missclassified = 1 - int(true == predicted)
        return missclassified

    @staticmethod
    def _calculate_new_weights(weights: List[float], beta: float, error: List[float]):
        """Update weights by multiplying weights with beta to the power of 1 - error."""
        return [w_i * beta ** (1 - err_i) for w_i, err_i in zip(weights, error)]

    @staticmethod
    def _normalize_weights(weights: List[float]):
        """Normalize weights. Formula: weights = weights / sum(weights)"""
        weight_sum = sum(weights)
        if weight_sum == 0:
            return [0 for _ in weights]
        return [w_i / weight_sum for w_i in weights]

    def predict(self, dataset: pd.DataFrame):
        return [
            self._classifiy_single_tuple(tuple.to_frame().T)
            for _, tuple in dataset.iterrows()
        ]

    def _classifiy_single_tuple(self, tuple: pd.DataFrame):
        # Initialize class weights:
        class_weights = {current_class: 0 for current_class in self.classes}

        # Calculate weight of each classifier's vote
        classifier_weight = [
            log(1 / beta_i, 2) if beta_i > 0 else 0 for beta_i in self.betas
        ]

        # Obtain predictions from all classifiers
        predicitons_per_classifier = [
            current_classifier.predict(tuple)[0]
            for current_classifier in self.classifiers
        ]

        # Update class weights
        for current_weight, current_prediction in zip(
            classifier_weight, predicitons_per_classifier
        ):
            class_weights[current_prediction] += current_weight

        # Return class with the highest weight
        return max(class_weights, key=class_weights.get)


if __name__ == "__main__":
    dataset = pd.read_csv("car_train.csv")
    test_dataset = pd.read_csv("car_test.csv")

    # target we want to predict
    target_attribute = "condition"

    # dataset.drop("Unnamed: 0", axis=1, inplace=True)
    # test_dataset.drop("Unnamed: 0", axis=1, inplace=True)
    # dataset.to_csv("car_train.csv", index=False)
    # test_dataset.to_csv("car_test.csv", index=False)

    # dataset = pd.read_csv("car.csv")
    # dataset.loc[dataset[target_attribute] != "unacc", target_attribute] = "acc"
    # print(dataset["condition"].unique())
    # print(dataset["condition"].value_counts())
    # # dataset.to_csv("car.csv", index=False)

    # train, test = train_test_split(dataset, test_size=0.3)
    # train.to_csv("car_train.csv", index=False)
    # test.to_csv("car_test.csv", index=False)

    adaboost = AdaBoost()
    adaboost.fit(dataset=dataset, target_attribute=target_attribute)

    print("predict")
    true_values = test_dataset.iloc[:, -1].tolist()
    predictions = adaboost.predict(test_dataset.iloc[:, :-1])
    # for true, predict in zip(true_values, predictions):
    #     print("True", true, "prediction", predict)

    print("Accuracy:", accuracy_score(y_true=true_values, y_pred=predictions))
