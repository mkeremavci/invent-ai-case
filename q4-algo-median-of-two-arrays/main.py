# © 2025 kerem.ai · All rights reserved.

import math
from collections import deque


def main() -> None:
    """
    Main function to run the program.
    This program takes two sorted arrays and returns the median of the concatenated arrays.
    Since the program expects the inputs to be sorted, if the input arrays are not sorted,
    the program will raise an error.
    The user is prompted to enter the two arrays, and the program returns the median of
    the concatenated arrays.
    Array elements must be space separated.
    Otherwise, the program will raise an error.

    Raises
    ------
    ValueError:
        If the user enters invalid input (e.g. non-numeric, non-space separated, non-sorted arrays,
        or both of the arrays are empty).
    """
    # Get the input from the user
    input1 = input("input1: ")
    input2 = input("input2: ")

    # Convert the input to a double ended queue of floats
    input1 = deque(map(float, input1.split()))
    input2 = deque(map(float, input2.split()))

    if not input1 or not input2:
        raise ValueError("At least one of the input arrays is empty.")

    # Get the total number of elements in the merged array
    num_elems = len(input1) + len(input2)
    median_lower_idx = math.floor((num_elems + 1) / 2)
    median_upper_idx = math.ceil((num_elems + 1) / 2)

    # Merge the two arrays and get the median
    merged_array: list[float] = []
    median = 0.0
    counter = 0
    denominator = 2.0 if num_elems % 2 == 0 else 1.0
    latest_elem = -1 * float(
        "inf"
    )  # To be used for checking if the input arrays are sorted

    while input1 or input2:  # While any of the input arrays are not empty
        # Get the current element from the input arrays
        if not input1:
            current_elem = input2.popleft()
        elif not input2:
            current_elem = input1.popleft()
        elif input1[0] < input2[0]:
            current_elem = input1.popleft()
        else:
            current_elem = input2.popleft()

        # Check if the input arrays are sorted
        if latest_elem > current_elem:
            raise ValueError(
                "The input arrays are not sorted. Please check your input."
            )
        latest_elem = current_elem

        # Add the current element to the merged array
        merged_array.append(current_elem)
        counter += 1

        # Check if the counter is equal to any median index
        if counter == median_lower_idx or counter == median_upper_idx:
            median += current_elem

    # Calculate the median
    median /= denominator
    print(f"median: {median}")


if __name__ == "__main__":
    # Run the main function
    main()
