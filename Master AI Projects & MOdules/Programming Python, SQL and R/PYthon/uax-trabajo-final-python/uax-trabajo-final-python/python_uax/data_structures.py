from typing import List, Dict, Tuple, Set


def reverse_list(l: List) -> List:

 return l[::-1]


def get_elements_between_positions(l: List, start: int, end: int = None) -> str:

    if start < 0 or (end is not None and end < 0):
        raise ValueError("Las posiciones deben ser enteros positivos")
    if start >= len(l) or (end is not None and end >= len(l)):
        raise ValueError("Las posiciones tienen que estar en el rango de la lista ")
    if end is None:
        end = start
    if start > end:
        raise ValueError("La posición inicial no puede ser mayor que la final")


    elements = l[start:end+1]
    return f"Elements between positions {start} and {end} (included): {elements}"







def get_number_of_times_number_appears_in_both_lists(l1: List[int], l2: List[int], n: int) -> int:
 if n not in l1 or n not in l2:
   return 0
 return min(l1.count(n), l2.count(n))


def get_names_of_adults(d: Dict[str, int]) -> List[str]:
    """
    Receives a dict[people, age] and returns the names of the people whose age is >= 18.

    >>> get_names_of_adults({'John': 16, 'Mary': 17, 'Peter': 18, 'Jane': 19, 'Mark': 20})
    ['Peter', 'Jane', 'Mark']

    >>> get_names_of_adults({'John': 16, 'Mary': 17, 'Peter': 18})
    ['Peter']

    >>> get_names_of_adults({'John': 16, 'Mary': 17})
    []

    :param d: dict[people, age]
    :return: Names of the people who are older than 18
    """
    return [people for people, age in d.items() if age >= 18]

def get_dict_items_by_keys(d: Dict, keys: List = None) -> List[Tuple]:
    """
    Receives a dict and an optional list, and returns a list of tuples where each tuple contains a key and a value
    from the dict whose key is in the list.

    >>> get_dict_items_by_keys({'a': 1, 'b': 2, 'c': 3, 'd': 4}, ['a', 'c'])
    [('a', 1), ('c', 3)]

    If the list is not provided, it is assumed to be the list of all the dict keys.

    >>> get_dict_items_by_keys({'a': 1, 'b': 2, 'c': 3, 'd': 4})
    [('a', 1), ('b', 2), ('c', 3), ('d', 4)]

    :param d: Dict
    :param keys: List of keys
    :return: List of tuples where each tuple contains a key and a value from the dict whose key is in the list
    """
    if keys is None:
      keys = d.keys()

    return [(key,d[key]) for key in keys if key in d]




def get_value_of_key_with_highest_number(d: Dict[int, str]) -> str:
    """
    Receives a dict[int, str] and returns the value of the key with the highest number.

    >>> get_value_of_key_with_highest_number({2: 'a', 4: 'b', 1: 'c', 3: 'd'})
    'b'

    >>> get_value_of_key_with_highest_number({2: 'a', 4: 'b', 1: 'c', 3: 'd', 5: 'e'})
    'e'

    :param d: dict[int, str]
    :return: Value of the key with the highest number
    """

    int_max = max(d.keys())
    return d[int_max]


def get_letters_in_first_word_but_not_in_second(first: str, second: str) -> Set[str]:
    """
    Receives two words and returns a list of the letters that are in the first word but not in the second.

    >>> get_letters_in_first_word_but_not_in_second('house', 'mouse')
    {'h'}

    >>> get_letters_in_first_word_but_not_in_second('house', 'home')
    {'u', 's'}

    >>> get_letters_in_first_word_but_not_in_second('house', 'house')
    set()

    :param first: First word
    :param second: Second word
    :return: List of letters that are in the first word but not in the second
    """
    ## Convierto las palabras en uan serie de letras unicas
    A= set(first)
    B= set(second)
    return A-B
