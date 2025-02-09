"""This is the main Ember file that calls all the 7 modules and runs the Ember system.
It is the main entry point for the Ember system.
"""
import os

def initializer():
    """
    When called, looks for a folder and create folders if not found.
    """
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists("logs"):
        os.makedirs("logs")
    if not os.path.exists("data/book_summerizer"):
        os.makedirs("data/book_summerizer")
    if not os.path.exists("data/book_summerizer/input_books"):
        os.makedirs("data/book_summerizer/input_books")
    if not os.path.exists("data/book_summerizer/summary"):
        os.makedirs("data/book_summerizer/summary")


def ember():
    print("Hello world!!!")
    initializer()
    return True

if __name__ == "__main__":

    ember()
