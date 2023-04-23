import requests
from bs4 import BeautifulSoup
import PyPDF2
import pdfplumber
from urllib.request import url2pathname
import torch

if torch.cuda.is_available():
    print("CUDA is enabled and available.")
    print("GPU:", torch.cuda.get_device_name(0))
else:
    print("CUDA is not available.")
from transformers import pipeline

def extract_html_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for script in soup(["script", "style"]):
        script.decompose()
    return ' '.join(soup.stripped_strings)

def extract_html_text_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    soup = BeautifulSoup(content, 'html.parser')
    for script in soup(["script", "style"]):
        script.decompose()
    return ' '.join(soup.stripped_strings)
def extract_pdf_text(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ' '.join(page.extract_text() for page in pdf.pages)
    return text
def extract_pdf_text_from_url(url):
    response = requests.get(url)
    with open("temp_pdf.pdf", "wb") as f:
        f.write(response.content)

    with pdfplumber.open("temp_pdf.pdf") as pdf:
        text = ' '.join(page.extract_text() for page in pdf.pages)
    return text
def tokenize(text, tokenizer):
    return tokenizer.encode(text, return_tensors="pt", add_special_tokens=True)

def split_text(text, tokenizer, max_length=1024):
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



def create_summary(text):
    device = 0 if torch.cuda.is_available() else -1
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=device)
    tokenizer = summarizer.tokenizer
    token_chunks = split_text(text, tokenizer, max_length=1000)

    summaries = []
    for chunk in token_chunks:
        chunk_text = tokenizer.decode(chunk, skip_special_tokens=True)
        summary_output = summarizer(chunk_text, max_length=100, min_length=25, do_sample=False)
        if summary_output:
            summaries.append(summary_output[0]['summary_text'].strip())

    # Join the summaries with newline characters to create paragraphs
    return "\n\n".join(summaries)

def main():
    url_or_path = input("Enter the URL or file path: ")

    if url_or_path.lower().endswith('.html'):
        if url_or_path.startswith('http://') or url_or_path.startswith('https://'):
            text = extract_html_text(url_or_path)
        else:
            if url_or_path.startswith('file://'):
                url_or_path = url_or_path[7:]
            file_path = url2pathname(url_or_path)
            text = extract_html_text_from_file(file_path)
    elif url_or_path.lower().endswith('.pdf'):
        if url_or_path.startswith('http://') or url_or_path.startswith('https://'):
            text = extract_pdf_text_from_url(url_or_path)
        else:
            if url_or_path.startswith('file://'):
                url_or_path = url_or_path[7:]
            file_path = url2pathname(url_or_path)
            text = extract_pdf_text(file_path)
    else:
        print("Unsupported file format")
        return

    summary = create_summary(text)
    print("\nSummary:\n", summary)
    # Save the summary to a file
    with open("summary.txt", "w", encoding="utf-8") as summary_file:
        summary_file.write(summary)

    # Print the summary
    print("Summary:")
    print(summary)
if __name__ == '__main__':
    main()
