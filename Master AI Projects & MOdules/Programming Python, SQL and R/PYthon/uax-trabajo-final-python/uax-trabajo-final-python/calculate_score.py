from xml.etree import ElementTree

# https://youtrack.jetbrains.com/issue/PY-49440/Inspection-doesnt-support-Pipenv-packaging
# noinspection PyPackageRequirements
from prettytable import PrettyTable


# Constants
RESULTS_XML = "Test Results - .xml"
MODULES_SCORE = {
    "data_structures": 2.5,
    "control_flow": 2.5,
    "functions": 1,
    "files": 1,
    "external_packages": 0.5,
    "classes": 2.5
}
SCORE_COLOR = {
    'fail': 'red',
    'pass': 'yellow',
    'excellent': 'green'
}

# Check that the XML file exists
try:
    open(RESULTS_XML)
except FileNotFoundError:
    print(cs('You have to run all the tests and export its results to an XML file first! '
             'See the `Calculate score` section in the README.md file.',
             color='orange'))
    raise

# Parse the XML file
tree = ElementTree.parse(RESULTS_XML)
root = tree.getroot()

# Create table object to display the results of each module
table = PrettyTable()
# Add columns
table.field_names = ["Module", "Score per test", "Num tests (passed / total)", "Score (actual / max)"]
# Customize appearance
table.align["Module"] = "l"

# Variables to store the totals
total_num_tests = 0
total_num_tests_passed = 0
total_max_score = sum(MODULES_SCORE.values())
total_actual_score = 0

# Iterate through top-level suites
suites = root.findall('./suite')
for suite in suites:
    suite_name = suite.get('name')
    module_name = suite_name[len('test_'):]

    # Count number of tests in the top-level suite
    num_tests = len(suite.findall('.//test'))
    total_num_tests += num_tests

    # Count number of passed tests in the top-level suite
    num_tests_passed = len(suite.findall('.//test[@status="passed"]'))
    total_num_tests_passed += num_tests_passed

    # Calculate the score of each test in the suite
    max_suite_score = MODULES_SCORE[module_name]
    score_per_test = max_suite_score / num_tests

    # Calculate the actual score of the suite based on the number of passed tests
    actual_suite_score = num_tests_passed * score_per_test
    total_actual_score += actual_suite_score

    # Check if the current iteration is the last one
    is_last = suite == suites[-1]

    # Add a row to the table
    table.add_row([module_name, f'{score_per_test:.3f}', f'{num_tests_passed} / {num_tests}', f'{actual_suite_score:.2f} / {max_suite_score:.2f}'],
                  divider=is_last)

# Add the totals to the table
total_actual_score_color = SCORE_COLOR['excellent' if total_actual_score >= 7.5 else 'pass' if total_actual_score >= 5 else 'fail']
total_actual_score_formatted = cs(f'{total_actual_score:.2f}', total_actual_score_color).bold().underline()
table.add_row(["Total", '', f'{total_num_tests_passed} / {total_num_tests}', f'{total_actual_score_formatted} / {total_max_score}'])

# Show the table
print(table)
