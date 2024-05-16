def testcase_prompt(problem, example_testcase):
    return f"""Given a question, you need to write several sets of test cases for checking the correctness of the code implementation about the functionality of the given question. Please do not duplicate the Example IO given in the question. You are required to generate at least 10 sets of test cases that comprehensively validate the implementation's functionality under various conditions, including but not limited to boundary test cases, functional correctness test cases, etc. The elements in each test case can only consist of two parts named 'caseIn' and 'caseOut'. Please also annotate each test case with detailed comments. Again, all you need to do and you can do is to return me only an array called test_cases consisting of caseIn and caseOut two parts.
Here is an example: 

# Problem:
def median(l):
    \"\"\"
    Given a list l, return median of elements in the list. 
    >>> median([3, 1, 2, 4, 5])
    3
    >>> median([-7, 4, 6, 100, 10, 20])
    15.0
    \"\"\"

# Test case:
test_cases = [
        ([[-10,4,6,1000,10,20]],[8.0]),
    ]
    
Each tuple in `test_cases` contains two parts: case_in and case_out, both of which are lists. Each element in the list corresponds to a parameter/return value of the function. For example, the first example IO in the problem description can be represented as: ([[3, 1, 2, 4, 5]], [3])

Now, please provide the test cases for the following problem. Please do not duplicate the Example I0 given in the question.

# Problem:
{problem}

For this problem, an example IO tuple can be represented as: {example_testcase}

# Test case:
"""


def specification_prompt(problem, refined_description=""):
    # No need to provide testcase format for humaneval
    if len(refined_description) > 0:
        problem = f"""{problem}

The following is a refined description of the problem:

{refined_description}
"""

    return f"""I want you to act as a python programmer. Given a problem, you need to generate two specification functions: `preconditions(caseIn)`, which checks whether the input (caseIn) satisfies certain constraints about the requeriement, and `postconditions(caseIn, caseOut)` checks the functional relationships between the test inputs (caseIn) and outputs (caseOut) to ensure compliance with the requirements. Please thoroughly assess the correctness of the test cases (caseIn and caseOut) from various perspectives, including but not limited to formal correctness, functional correctness, logical correctness, etc. In the event that an error is encountered during the evaluation, please print the corresponding test case along with a specific error message. Please also generate as many detailed comments as possible.
Here is an example:

# Problem:
def median(l):
    \"\"\"
    Given a list l, return median of elements in the list. 
    >>> median([3, 1, 2, 4, 5])
    3
    >>> median([-7, 4, 6, 100, 10, 20])
    15.0
    \"\"\"

# Specification:
def preconditions(l):
    assert isinstance(l, list), "Input is not a list."
    assert all([isinstance(i, (int, float)) for i in l]), "There are elements in input that are not of type int or float."
def postconditions(l, output):
    assert isinstance(output, (int, float)), "There are elements in output that are not of type int or float."
    num_greater = sum([1 for i in l if i >= output])
    num_less = sum([1 for i in l if i <= output])
    assert num_greater == num_less, "Counts of elements greater than or equal to 'output' and less than or equal to 'output' are not equal."

Now, please provide the specifications for the following problem. Your output should only include two functions: "preconditions(caseIn)" and "postconditions(caseIn, caseOut)". You do not need to generate test cases. Only provide the code.

# Problem:
{problem}

# Specification:
"""


def specification_modify_prompt_for_proper_testcase(param_names, testcase_info):
    prompt = "I have tested your specification using some correct testcases to ensure its completeness. If your specification is complete, there should be no errors reported. Please modify your specification according to the following messages:"
    for case_in, case_out, msg in testcase_info:
        msg_item = "\nwhen "
        for params_name, param_value in zip(param_names, case_in):
            msg_item += f"{params_name} = {param_value}, "
        msg_item += f"output = {case_out[0]}, the specification erroneously reports: {msg}"
        prompt += msg_item
    return prompt


def specification_modify_prompt_for_improper_testcase(param_names, testcase_info):
    prompt = "I have tested your specification using some wrong cases to ensure its soundness. If your specification is sound, there should be some errors reported. Please modify your specification according to the following messages:"
    for case_in, case_out in testcase_info:
        msg_item = "\nwhen "
        for params_name, param_value in zip(param_names, case_in):
            msg_item += f"{params_name} = {param_value}, "
        msg_item += f"output = {case_out[0]}, this case erroneously passed the specification"
        prompt += msg_item
    return prompt


def requirement_refine_prompt(problem):
    # No need to describe format for humaneval
    return f"""Given a problem description, you need to itemize its requirements to make it easier to understand. Here is an example:

# Problem:
def median(l):
    \"\"\"
    Given a list l, return median of elements in the list. 
    >>> median([3, 1, 2, 4, 5])
    3
    >>> median([-7, 4, 6, 100, 10, 20])
    15.0
    \"\"\"

# Refined requirements:

## Problem description:
This problem requires writing a function to determine the median of a given list of numbers. The median is the middle number in a sorted, ascending or descending, list of numbers and can be more descriptive of that data set than the average. If the list has an odd number of elements, the median is the middle element. If the list has an even number of elements, the median is the average of the two middle elements.

## Data restrictions:
The list l can contain any number of integers or floats.
The list will contain at least one element.
The elements of the list can be negative or positive.

## Explanation of examples:
For median([3, 1, 2, 4, 5]), the sorted list is [1, 2, 3, 4, 5]. The middle element is 3, so the output should be 3.
For median([-7, 4, 6, 100, 10, 20]), the sorted list is [-7, 4, 6, 10, 20, 100]. The two middle elements are 6 and 10, and their average is (6 + 10) / 2 = 8.0, so the output should be 8.0.

Now please refine the requirements as required without changing the meaning of the problem to make it clearer and more understandable. Note that you can't add or delete any conditions and contents in the problem description.

# Problem:
{problem}

# Refined requirements:
"""