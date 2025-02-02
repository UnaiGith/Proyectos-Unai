from typing import List, Callable


def concat_words_with_prefix(prefix: str, *words: str) -> List[str]:
    """
    Receives a prefix and an indeterminate number of words and returns
    a list with the concatenation of the prefix and each word.

    >>> concat_words_with_prefix('super', 'hero')
    ['superhero']

    >>> concat_words_with_prefix('super', 'hero', 'star')
    ['superhero', 'superstar']

    >>> concat_words_with_prefix('super', 'hero', 'star', 'power')
    ['superhero', 'superstar', 'superpower']

    >>> concat_words_with_prefix('sub', 'marine', 'way', 'title')
    ['submarine', 'subway', 'subtitle']

    :param prefix: Prefix
    :param words: Words
    :return: List with the concatenation of the prefix and each word
    """
    return [prefix + word for word in words]


def make_multiplier_of(n: int) -> Callable[[int], int]:
    """
    Receives a number and returns a function that receives another number
    and multiplies the seconds number by the first.

    >>> times_3 = make_multiplier_of(3)
    >>> times_3(2)
    6
    >>> times_3(3)
    9

    >>> times_5 = make_multiplier_of(5)
    >>> times_5(2)
    10
    >>> times_5(3)
    15

    :param n: Number
    :return: Function that receives another number and multiplies the seconds number by the first
    """
    def multiplication(x: int)-> int:
        return n*x

    return multiplication


