import os.path


def append_to_file(text: str):



# Function to append text to a file

    file_path = 'file.txt'
    # Open the file in append mode, which creates the file if it doesn't exist
    with open(file_path, 'a') as file:
        file.write(text + '\n')  # Write the text followed by a newline character

# Function to read the content of a file



def read_file() -> str:
    """
    Reads the content of a file named 'file.txt' and returns it.

    If the file doesn't exist, the string 'File not found!' is returned.

    >>> read_file()
    'File not found!'

    >>> append_to_file('First line')
    >>> read_file()
    'First line\\n'

    >>> append_to_file('Second line')
    >>> read_file()
    'First line\\nSecond line\\n'

    :return: Content of the file 'file.txt'
    """
    file_path = 'file.txt'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    else:
        return 'File not found!'

