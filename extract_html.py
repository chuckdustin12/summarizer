import unittest
import requests
from summarizer import extract_pdf_text

class TestPdfTextExtraction(unittest.TestCase):

    def test_extract_pdf_text(self):
        url = "https://www.sec.gov/rules/sro/nscc/2023/34-97249.pdf"
        with requests.get(url, stream=True) as r:
            with open("test.pdf", "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        result = extract_pdf_text("test.pdf")
        cleaned_text = result.replace('\n', ' ').replace('\r', '').strip()
        paragraphs = [p.strip() for p in cleaned_text.split('\n\n') if len(p.strip()) > 0]
        formatted_text = '\n\n'.join(paragraphs)
        with open("output.txt", "w") as f:
            f.write(formatted_text)
        self.assertTrue(cleaned_text.startswith("SECURITIES AND EXCHANGE COMMISSION"))

if __name__ == '__main__':
    unittest.main()