"""
This is first step in the workflow of the Ember system. 
The main focus is to read the "input_books" and generate summary and metadta for those books
"""

from pathlib import Path
from PyPDF2 import PdfReader

def get_map_of_books(input_folder='input_books'):
    """
    Returns a dictionary mapping book names to their absolute file paths.
    
    Example:
        {
            "book1": "C:/path/to/input_books/book1.pdf",
            "book2": "C:/path/to/input_books/book2.epub",
            ...
        }
    """
    input_path = Path(input_folder)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Folder '{input_folder}' does not exist.")
    if not input_path.is_dir():
        raise NotADirectoryError(f"'{input_folder}' is not a directory.")
    
    return {file.stem: str(file.resolve()) for file in input_path.iterdir() if file.is_file()}

def read_pdf_as_string(pdf_path):
    """
    Reads a PDF file and returns its content as a single string.

    Parameters:
    - pdf_path (str): The path to the PDF file.

    Returns:
    - str: The entire content of the PDF as a single string.
    """
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"  # Add page break for clarity

    return text.strip()

def get_number_of_chapters(book_path):
    """
    Returns the number of chapters in a book.
    """
    pdf_content = read_pdf_as_string(book_path)
    print(pdf_content[:1000])  

def summerizer():
    print("welcome sumemrizer")
    # 1 Read the input folder and get a list of all book names
    books = get_map_of_books('data/book_summerizer/input_books') # TODO : remove hardcode
    # 2 iterate through each book 
    for book,book_path in books.items():
        print(f"Processing book: {book}")
        # 2.1 generate sumamry and metadata for each book
            # 2.1.1 figure out how many chpaters or parts in book
        get_number_of_chapters(book_path)
            # 2.1.2 read each chapter and generate summary
        # 2.2 save the summary and metadata to codex file in sumamry folder 
        # 2.3 move the book from input folder to sumamry folder
        # 2.4 update the token file that the processing of sumemrization is complete
    return True



if __name__=="__main__":
    summerizer()