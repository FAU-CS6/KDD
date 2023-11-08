import pandas as pd
from typing import List, Any, Callable, Tuple

from .attribute_selection_method import random_attribute_selection
from .tree_utils import Node, Branch


class DecisionTree:
    """Basic Decision Tree algorithm."""

    def __init__(
        self,
        attribute_selection_method: Callable = random_attribute_selection,
        depth: int = 3,
    ) -> None:
        self.attribute_selection_method = attribute_selection_method
        self.depth: int = depth  # set to -1 if you want to have a full sized tree

        # Function fit will later populate this variable
        self.target_attribute = None

        # Function fit will later produce a decision tree
        self.tree: Node = None

    def fit(
        self,
        dataset: pd.DataFrame,
        target_attribute: str,
    ) -> None:
        """Fit decision tree on a given dataset and target attribute."""
        # Store target_attribute in this object
        self.target_attribute = target_attribute
        # Get the attribute list
        attribute_list = [col for col in dataset.columns if col != target_attribute]
        # Construct the actual decision tree
        self.tree = self._build_tree(dataset, attribute_list, depth=0)

    def _build_tree(
        self, data: pd.DataFrame, attribute_list: List[str], depth: int = 0
    ) -> Node:
        """'Private' method to build decision tree recursively. Returns current (sub-)tree at point."""
        if len(data[self.target_attribute].unique()) == 1:
            # All tuples have same class, thus return node as leaf node labeled with this class
            return Node(label=data[self.target_attribute].unique()[0])

        if not attribute_list or self.depth == depth:
            # List is empty, return leaf node with majority class
            majority_class = (
                data[self.target_attribute]
                .value_counts()
                .sort_values(ascending=False)
                .index[0]
            )
            return Node(label=majority_class)

        # Determine splitting attribute
        splitting_attribute, labels = self._find_best_splitting_attribute(
            data, attribute_list
        )

        # Typically, we have to determine if the splitting attribute is discrete valued,
        # but we restrict ourselves here only to discrete-valued data.
        # Yet, we need to check if the attribute_selection_method allows multiway splits.
        # For instance, Gini index only allows binary trees, thus, we can only remove the
        # splitting attribute from the attribute list when we do not have Gini index as the
        # attribute selection method.
        if self.attribute_selection_method.__name__ != "gini_index" or (
            labels and len(labels) == 1
        ):
            # Remove the splitting_attribute from attribute_list
            attribute_list = [
                attr for attr in attribute_list if attr != splitting_attribute
            ]

        # Create a node with an empty list as branches
        node = Node(splitting_attribute, [])

        if self.attribute_selection_method.__name__ == "gini_index":
            attribute_values = labels
        else:
            attribute_values = [[value] for value in data[splitting_attribute].unique()]

        # For each unique value of this splitting_attribute
        for value in attribute_values:
            # Partition the tuples and grow subtrees for each partition
            partition: pd.DataFrame = data[data[splitting_attribute].isin(value)]
            if partition.empty:
                # Attach a leaf labeled with the majority class
                node.branches.append(Node(value))
            else:
                # Append the node returned by _build_tree.
                # Note that we need to copy the list of attributes otherwise we would perform the following
                # operations on the very same attribute list. This can be done by slicing, but
                # also by using the built in function copy().
                node.branches.append(
                    Branch(
                        label=value,
                        node=self._build_tree(
                            data=partition,
                            attribute_list=attribute_list[:],
                            depth=depth + 1,
                        ),
                    )
                )
        return node

    def _find_best_splitting_attribute(
        self, data: pd.DataFrame, attribute_list: List[str]
    ) -> tuple[str, Any]:
        """'Private' method to find the best splitting attribute in a list of all available attributes."""
        # For each attribute in the given attribute_list calculate a scalar value that
        # is later then used to determine the best splitting attribute.
        # Here, we build a list of tuples. One such tuple contains the attribute name as
        # well the calculated scalar value.
        # Note that in the case of Gini index as the attribute selection method, a list
        # of attribute values and a scalar value such as
        # [[['high'], ['medium', 'low']], 0.4428571428571429] is returnd.
        all_split_information = [
            (
                attribute,
                self.attribute_selection_method(
                    dataset=data,
                    target_attribute=self.target_attribute,
                    partition_attribute=attribute,
                ),
            )
            for attribute in attribute_list
        ]
        # Above list comprehension is the same as:
        # all_split_information = []
        # for attribute in attribute_list:
        #     all_split_information.append(
        #         (
        #             attribute,
        #             self.attribute_selection_method(
        #                 dataset=data,
        #                 target_attribute=self.target_attribute,
        #                 partition_attribute=attribute,
        #             ),
        #         )
        #     )

        # Test if our attribute_selection_method is the Gini index,
        # otherwise it must be one of the other measures.
        if self.attribute_selection_method.__name__ == "gini_index":
            # Sort this list of tuples based on the scalar value
            sorted_information = sorted(all_split_information, key=lambda x: x[1][-1])
            # When using Gini index, we want to maximize the information needed and thus need to select
            # the minimum value. This is the first element and it may look like
            # ('income', ([['high'], ['medium', 'low']], 0.375)).
            # We therefore, want to return the attribute name and the labels.
            return sorted_information[0][0], sorted_information[0][1][0]
        # "Else": Another measure has been used.
        # It is not wrong to explicitly write else here. Yet it is not really needed in this particular case.
        # Sort this list of tuples based on the scalar value
        sorted_information = sorted(all_split_information, key=lambda x: x[1])
        # When using information gain or gain ratio we want to minimize the information needed
        # to classify a tuple/row, meaning we have to select the element in sorted_information with
        # the highest value. In our variable sorted_information it is the last Python tuple element ([-1]).
        return sorted_information[-1]

    def predict(self, dataset: pd.DataFrame) -> List[Any]:
        """Returns predicted values for a given dataset."""
        if self.tree is None:
            raise ValueError(
                "DecisionTree not trained on data. Call function fit() first."
            )
        return [self._dfs(self.tree, row) for _, row in dataset.iterrows()]

    def _dfs(self, node: Node, data_row: pd.Series):
        """Private method to recursively walk down our decision tree to obtain a signle class label."""
        # If a Branch contains an empty list or is None, return its node label.
        if not node.branches:
            return node.label

        # Obtain the corresponding value of our tuple/sample of the column
        # that is specified in our node label.
        value = data_row[node.label]

        # Iterate over each branch of the current node.
        for branch in node.branches:
            if value in branch.label:
                # If the current branch label is equal to the dataset's corresponding
                # column value then go level down in the tree.
                return self._dfs(branch.node, data_row)
