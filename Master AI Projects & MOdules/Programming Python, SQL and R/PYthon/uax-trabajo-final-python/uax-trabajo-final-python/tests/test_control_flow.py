import re
import unittest
from ast import Constant, Expr, FunctionDef, Module, parse
from inspect import getsource
from textwrap import dedent
from typing import cast, Callable

from python_uax.control_flow import check_number, get_full_names_and_adults_using_for_loop, get_sum_of_numbers_until_n_using_while_loop, \
    get_daily_activities_using_match


class ControlFlowTestCase(unittest.TestCase):
    def test_check_number(self):
        self.assertEqual('Positive', check_number(1))
        self.assertEqual('Negative', check_number(-1))
        self.assertEqual('Zero', check_number(0))

    def test_get_sum_of_numbers_until_n_using_while_loop(self):
        self.assertEqual(0, get_sum_of_numbers_until_n_using_while_loop(0))
        self.assertEqual(1, get_sum_of_numbers_until_n_using_while_loop(1))
        self.assertEqual(3, get_sum_of_numbers_until_n_using_while_loop(2))
        self.assertEqual(6, get_sum_of_numbers_until_n_using_while_loop(3))
        self.assertEqual(10, get_sum_of_numbers_until_n_using_while_loop(4))
        self.assertEqual(15, get_sum_of_numbers_until_n_using_while_loop(5))
        self.assertEqual(55, get_sum_of_numbers_until_n_using_while_loop(10))
        self.assertEqual(210, get_sum_of_numbers_until_n_using_while_loop(20))

        # Assert that the function uses a while loop
        self.assert_function_contains_control_flow(get_sum_of_numbers_until_n_using_while_loop, 'while')

    def test_get_full_names_and_adults_using_for_loop(self):
        self.assertEqual(
            [('John Smith', False), ('Mary Johnson', False), ('Peter Williams', True), ('Jane Jones', True), ('Mark Brown', True)],
            get_full_names_and_adults_using_for_loop(
                [('John', 'Smith', 16), ('Mary', 'Johnson', 17), ('Peter', 'Williams', 18), ('Jane', 'Jones', 19), ('Mark', 'Brown', 20)]))
        self.assertEqual([('John Smith', False)], get_full_names_and_adults_using_for_loop([('John', 'Smith', 16)]))
        self.assertEqual([], get_full_names_and_adults_using_for_loop([]))

        # Assert that the function uses a for loop
        self.assert_function_contains_control_flow(get_full_names_and_adults_using_for_loop, 'for')

        # Assert that the function does not use list comprehension
        self.assert_function_does_not_use_list_comprehension(get_full_names_and_adults_using_for_loop)

    def test_get_daily_activities_using_match(self):
        self.assertEqual('planning', get_daily_activities_using_match('monday'))
        self.assertEqual('meetings', get_daily_activities_using_match('tuesday'))
        self.assertEqual('meetings', get_daily_activities_using_match('wednesday'))
        self.assertEqual('coding', get_daily_activities_using_match('thursday'))
        self.assertEqual('testing', get_daily_activities_using_match('friday'))
        self.assertEqual('rest', get_daily_activities_using_match('saturday'))
        self.assertEqual('rest', get_daily_activities_using_match('sunday'))

        # Assert that the function uses a match statement
        self.assert_function_contains_control_flow(get_daily_activities_using_match, 'match')

    # region ------------ Custom assert methods ------------

    def assert_function_contains_control_flow(self, function: Callable, control_flow: str) -> None:
        # Get the source code of the function (without docstrings and comments)
        function_source = get_function_source_code(function)

        # Assert that the control flow statement is present in the source code as a whole word
        self.assertTrue(control_flow in function_source.split(), msg=f'You must use the {control_flow} statement')

    def assert_function_does_not_use_list_comprehension(self, function: Callable) -> None:
        # Get the source code of the function (without docstrings and comments)
        function_source = get_function_source_code(function)

        # Assert that the list comprehension is not present in the source code
        pattern = r'\[.*\s+for\s+.*\]'
        self.assertFalse(bool(re.search(pattern, function_source)), msg="You can't use list comprehension")

    # endregion


def get_function_source_code(function: Callable) -> str:
    """
    Returns the source code of a function without docstrings and comments.

    Based on https://stackoverflow.com/a/77154150.

    :param function: The function to get the source code from.
    :return: The source code of the function without docstrings and comments.
    """

    # Get cleanly indented source code of the function
    function_source = dedent(getsource(function))

    # Parse the source code into an Abstract Syntax Tree
    # The root of this tree is a Module node
    module: Module = parse(function_source)

    # The first child of a Module node is FunctionDef node that represents
    # the function definition. We cast module.body[0] to FunctionDef for type safety.
    function_def = cast(FunctionDef, module.body[0])

    # The first statement of a function could be a docstring, which in AST is represented as an Expr node
    # To remove the docstring, we need to find this Expr node
    first_stmt = function_def.body[0]

    # Check if the first statement is a docstring (a constant str expression)
    if (
            isinstance(first_stmt, Expr)
            and isinstance(first_stmt.value, Constant)
            and isinstance(first_stmt.value.value, str)
    ):
        # Split the original source code by lines
        code_lines: list[str] = function_source.splitlines()

        # Delete the lines corresponding to the docstring from the list
        # Note: We are using 0-based list index, but the line numbers in the parsed AST nodes are 1-based
        # So, we need to subtract 1 from the 'lineno' property of the node
        del code_lines[first_stmt.lineno - 1: first_stmt.end_lineno]

        # Join the remaining lines back into a single string
        function_source = '\n'.join(code_lines)

    # Remove one line comments
    function_source = '\n'.join(
        line for line in function_source.splitlines() if not line.strip().startswith('#'))
    # Remove inline comments
    function_source = re.sub(r'#.*', '', function_source)

    # Return the source code of the function without docstrings and comments
    return function_source


if __name__ == '__main__':
    unittest.main()
