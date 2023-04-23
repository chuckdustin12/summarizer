import requests
from bs4 import BeautifulSoup
import pdfplumber
import torch

if torch.cuda.is_available():
    print("CUDA is enabled and available.")
    print("GPU:", torch.cuda.get_device_name(0))
else:
    print("CUDA is not available.")


def extract_html_text(url):
    """
    Extracts the text from a HTML page at the specified URL.

    Args:
        url (str): The URL of the HTML page to extract text from.

    Returns:
        str: The extracted text.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for script in soup(["script", "style"]):
        script.decompose()
    return ' '.join(soup.stripped_strings)


def extract_html_text_from_file(file_path):
    """
    Extracts the text from a HTML file at the specified file path.

    Args:
        file_path (str): The file path of the HTML file to extract text from.

    Returns:
        str: The extracted text.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    soup = BeautifulSoup(content, 'html.parser')
    for script in soup(["script", "style"]):
        script.decompose()
    return ' '.join(soup.stripped_strings)


def extract_pdf_text(file_path):
    """
    Extracts the text from a PDF file at the specified file path.

    Args:
        file_path (str): The file path of the PDF file to extract text from.

    Returns:
        str: The extracted text.
    """
    with pdfplumber.open(file_path) as pdf:
        text = ' '.join(page.extract_text() for page in pdf.pages)
    return text


def extract_pdf_text_from_url(url):
    """
    Extracts the text from a PDF file at the specified URL.

    Args:
        url (str): The URL of the PDF file to extract text from.

    Returns:
        str: The extracted text.
    """
    response = requests.get(url)
    with open("temp_pdf.pdf", "wb") as f:
        f.write(response.content)

    with pdfplumber.open("temp_pdf.pdf") as pdf:
        text = ' '.join(page.extract_text() for page in pdf.pages)
    return text


def tokenize(text, tokenizer):
    """
    Tokenizes the specified text using the specified tokenizer.

    Args:
        text (str): The text to tokenize.
        tokenizer: The tokenizer to use.

    Returns:
        torch.Tensor: The tokenized text.
    """
    return tokenizer.encode(text, return_tensors="pt", add_special_tokens=True)


def split_text(text, tokenizer, max_length=1024):
    """
    Splits the specified text into chunks of the specified maximum length.

    Args:
        text (str): The text to split.
        tokenizer: The tokenizer to use.
        max_length (int): The maximum length of each chunk.

    Returns:
        list: A list of tokenized text chunks.
    """
    tokens = tokenize(text, tokenizer)
    token_chunks = []
    current_chunk = []

    for token in tokens[0]:
        if len(current_chunk) + 1 <= max_length:
            current_chunk.append(token.item())
        else:
            token_chunks.append(current_chunk)
            current_chunk = [token.item()]

    if current_chunk:
        token_chunks.append(current_chunk)

    return token_chunks