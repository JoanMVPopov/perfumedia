def calculate_notes_jaccard(list_i, list_j):
    """
        Compute Jaccard similarity between two binary lists.

        Args:
            list1 (list): First list of 0s and 1s.
            list2 (list): Second list of 0s and 1s.

        Returns:
            float: Jaccard similarity between the two lists.

        Raises:
            ValueError: If lists have different lengths or contain invalid values.
        """
    if len(list_i) != len(list_j):
        raise ValueError("Both lists must have the same length.")

    # validate inputs
    if not all(x in (0, 1) for x in list_i) or not all(x in (0, 1) for x in list_j):
        raise ValueError("Lists must contain only 0s and 1s.")

    # get indices where value is 1
    set1 = set(i for i, val in enumerate(list_i) if val == 1)
    set2 = set(i for i, val in enumerate(list_j) if val == 1)

    # calculate intersection and union using set operations
    intersection = len(set1 & set2)
    union = len(set1 | set2)

    return intersection / union if union != 0 else 0.0


def calculate_manhattan(list_i, list_j, max_diff):
    if len(list_i) != len(list_j):
        raise ValueError("Sequences must have equal length")
    if not list_i or not list_j:
        raise ValueError("Sequences cannot be empty")

    # compute the L1 (Manhattan) distance
    diff = sum(abs(ai - bi) for ai, bi in zip(list_i, list_j))

    return 1 - (diff / max_diff) if max_diff != 0 else 0