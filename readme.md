Text Extraction and Tokenization
This program extracts text from HTML and PDF files, as well as from HTML and PDF files available at a URL. It then tokenizes the extracted text using the Transformers library.

Requirements
Python 3.x
Required Python packages can be installed using pip by running the following command:

Copy code
pip install -r requirements.txt
Usage
The following functions are available in the program:

extract_html_text(url): Extracts text from a HTML page at the specified URL.
extract_html_text_from_file(file_path): Extracts text from a HTML file at the specified file path.
extract_pdf_text(file_path): Extracts text from a PDF file at the specified file path.
extract_pdf_text_from_url(url): Extracts text from a PDF file at the specified URL.
tokenize(text, tokenizer): Tokenizes the specified text using the specified tokenizer.
split_text(text, tokenizer, max_length=1024): Splits the specified text into chunks of the specified maximum length.
You can import these functions into your Python code and use them as required.

Here's an example of how to use the extract_html_text() function:

python
Copy code
import requests
from text_extraction import extract_html_text

url = "https://www.example.com"
text = extract_html_text(url)
print(text)
Here's an example of how to use the extract_pdf_text_from_url() function:

python
Copy code
import requests
from text_extraction import extract_pdf_text_from_url

url = "https://www.example.com/example.pdf"
text = extract_pdf_text_from_url(url)
print(text)
License
This program is licensed under the MIT License.