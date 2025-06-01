# invent-ai-case

In this project, I have solved the problems shared by Invent AI.
I could choose one of the algorithm problems to solve, and 
I decided to solve [Q4](q4-algo-median-of-two-arrays/description.md).
[Q5](q5-dataeng-forecasting-features/description.md) was mandatory.


## Environment Setup

To run the programs, you need to have Python 3.11 or higher installed.
However, it is recommended to use Python 3.11 since the code is written in Python 3.11.

### Recommended Setup (conda)

You can install Python 3.11 and the dependencies by using
[conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) with the following command:

```bash
conda env create -f environment.yml
```

This command will create a new conda environment with the name `invent-ai`.
You can activate the environment by executing the following command:

```bash
conda activate invent-ai
```

After activating the environment, you can continue with the following steps.

### Alternative Setup (venv)

If you want to use venv instead of conda, please ensure that the version of Python is 3.11 or higher.
You can create a new venv by executing the following command:

```bash
python -m venv invent-ai
```

You can activate the environment by executing the following command:

```bash
source invent-ai/bin/activate
```

After activating the environment, please install the dependencies by executing the following command:

```bash
pip install -r requirements.txt
```


## Q4 - Median of Two Sorted Arrays

In this problem, it is expected to merge two sorted arrays (which are given by the user)
into a single sorted array and return the median of the merged array.
Since it is given that the arrays are already sorted,
the problem can be solved in $O(n)$ time complexity.

I have implemented the solution in [main.py](q4-algo-median-of-two-arrays/main.py).
You can run the program by executing the following command:

```bash
python q4-algo-median-of-two-arrays/main.py
```

Inputs are expected to be entered as space separated lists of numbers
from the user. If the inputs are not valid, the program will raise an error.
Exceptions are listed below:

- If the user enters non-numeric values, the program will raise an error.
- If the user enters non-space separated values, the program will raise an error.
- If the user enters non-sorted arrays, the program will raise an error.
- If the user enters empty arrays (both of the arrays are empty), the program will raise an error.

### Time Complexity

The time complexity of the solution is $O(n)$ where $n$ is the total number of elements in the merged array.
The arrays are stored in a double ended queue, a.k.a. deque,
which enables efficient insertion and deletion from both ends.
It is crucial to use a deque instead of a list,
since the list.pop() operation has a time complexity of $O(n)$
for the first element, which is not efficient for this problem.
The median is calculated while merging the arrays.
So, actually, we do not need to iterate over both of the arrays to finish the merging (since the input arrays are sorted).
However, in the problem description, it is expected to merge the arrays,
so I have implemented the solution in a way that merges the arrays.


## Q5 - Data Engineering - Forecasting Features

In this problem, I was supposed to calculate the features for the forecasting model.
The features are calculated for the product, brand, and store level
for the desired time period.
Start and end dates (inclusive) should be passed as command line arguments.
After the features are calculated, the WMAPE is calculated using the features.

To run the program without any errors, the data structure should be as follows:

```
invent-ai-case
├── q3-algo-longest-substring-no-dup
├── q4-algo-median-of-two-arrays
├── q5-dataeng-forecasting-features
│   ├── input_data
│   │   └── data 
│   │       ├── brand.csv
│   │       ├── product.csv
│   │       ├── store.csv
│   │       └── sales.csv
│   ├── ...
│   ├── output_data
│   ├── src
│   └── main.py
├── ...
└── README.md
```

The input data should be placed in `q5-dataeng-forecasting-features/input_data/data` directory, as given in the repository.
The output data will be saved to `q5-dataeng-forecasting-features/output_data` directory.

You can run the program by executing the following command:

```bash
python q5-dataeng-forecasting-features/main.py --min-date <start_date> --max-date <end_date> --top <top_n>
```

Start and end dates should be in the format `YYYY-MM-DD`,
and top N should be a positive integer.
Otherwise, the program will raise an error.
You may not pass any arguments, and the program will use the default values.
The default values are:

- min-date: 2021-01-01
- max-date: 2021-05-30
- top: 5

### Object Oriented Programming (OOP)

The task is a straightforward, one-time data processing pipeline with no iterative components,
object interactions, or state management requirements.
While the problem description suggests applying OOP principles,
doing so in this specific case would be inefficient and artificial:

- There is no conceptual benefit from OOP since there are no reusable object types or behaviors,
no need to manage internal state, and no inter-object relationships that would justify class-based design.
- Introducing classes would increase memory usage and execution time,
without offering clarity or modularity benefits.
It would be a forced design decision for a task that is inherently procedural.
- Abstraction is still used in this implementation — at the function level.
One key function, used three times with different arguments, was abstracted out for reuse and clarity.
This reflects appropriate use of abstraction without overengineering.
