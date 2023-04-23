import unittest
import requests
import re
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

        # Formatting text for professional presentation
        sections = formatted_text.split('I. ')
        formatted_sections = ['I. ' + section.replace('  ', '\n    • ') for section in sections[1:]]
        intermediate_output = "\n\n".join(formatted_sections)

        # Adding more paragraphs by splitting at periods followed by an uppercase letter
        final_output = re.sub(r'\. ([A-Z])', r'.\n\n\1', intermediate_output)

        with open("output.txt", "w") as f:
            f.write(final_output)
        self.assertTrue(cleaned_text.startswith("SECURITIES AND EXCHANGE COMMISSION"))

if __name__ == '__main__':
    unittest.main()