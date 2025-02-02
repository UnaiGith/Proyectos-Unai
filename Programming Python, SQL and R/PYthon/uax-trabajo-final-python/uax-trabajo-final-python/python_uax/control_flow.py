from typing import List, Tuple


def check_number(n: int) -> str:
    """
    Receives an int and returns a string that specifies if the number is positive, negative or zero.


    :param n: Int number
    :return: String that specifies if the number is positive, negative or zero
    """

    if n > 0:
        return "Positive"
    elif n < 0:
        return "Negative"
    else:
        return "Zero"

def get_sum_of_numbers_until_n_using_while_loop(n: int) -> int:
    """
    Returns the sum of the first n natural numbers.

    IMPORTANT: This function must use a while loop.

    >>> get_sum_of_numbers_until_n_using_while_loop(1)
    1

    >>> get_sum_of_numbers_until_n_using_while_loop(2)
    3

    >>> get_sum_of_numbers_until_n_using_while_loop(3)
    6

    >>> get_sum_of_numbers_until_n_using_while_loop(10)
    55
    """
    contador=1
    sum=0
    while contador <= n:
      sum += contador
      contador += 1

    return sum

def get_full_names_and_adults_using_for_loop(people: List[Tuple[str, str, int]]) -> List[Tuple[str, bool]]:
    """
    Receives a list of tuples of 3 elements (name, surname, age) and returns a list of tuples of 2 elements
    (full_name, is_adult) where full_name is the concatenation of name and surname, and is_adult is a boolean
    that is True if the person's age is >= than 18.

    IMPORTANT: This function must use a for loop.

    >>> get_full_names_and_adults_using_for_loop([('John', 'Smith', 16), ('Mary', 'Johnson', 17), ('Peter', 'Williams', 18), ('Jane', 'Jones', 19),
    ...                                          ('Mark', 'Brown', 20)])
    [('John Smith', False), ('Mary Johnson', False), ('Peter Williams', True), ('Jane Jones', True), ('Mark Brown', True)]

    >>> get_full_names_and_adults_using_for_loop([('John', 'Smith', 16)])
    [('John Smith', False)]

    >>> get_full_names_and_adults_using_for_loop([])
    []
    """
    result=[]
    for name, surname, age in people:
       full_name= name+' '+surname
       is_adult=(age >=18)
       result.append((full_name, is_adult))
    return result




def get_daily_activities_using_match(day: str) -> str:
    """
    Receives a string that specifies a day of the week and returns a string that specifies the activity that is planned for that day.

    IMPORTANT: This function must use a match statement.

    >>> get_daily_activities_using_match('Monday')
    'planning'

    >>> get_daily_activities_using_match('Tuesday')
    'meetings'

    >>> get_daily_activities_using_match('Saturday')
    'rest'

    :param day: String that specifies a day of the week
    :return: String that specifies the activity planned for that day
    """
    match day.lower():
        case 'monday':
            return "planning"
        case 'tuesday':
            return "meetings"
        case 'wednesday':
            return "meetings"
        case 'thursday':
            return "coding"
        case 'friday':
            return "testing"
        case 'saturday':
            return "rest"
        case 'sunday':
            return "rest"
        case _:
            return "Invalid day"






