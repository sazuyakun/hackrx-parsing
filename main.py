from parser.PDFParser import PDFParser
from dotenv import load_dotenv
import os

load_dotenv()

LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")


# Example usage
if __name__ == "__main__":
    parser = PDFParser(api_key=LLAMA_CLOUD_API_KEY)

    pdf_url = "https://hackrx.blob.core.windows.net/assets/Arogya%20Sanjeevani%20Policy%20-%20CIN%20-%20U10200WB1906GOI001713%201.pdf?sv=2023-01-03&st=2025-07-21T08%3A29%3A02Z&se=2025-09-22T08%3A29%3A00Z&sr=b&sp=r&sig=nzrz1K9Iurt%2BBXom%2FB%2BMPTFMFP3PRnIvEsipAX10Ig4%3D"

    result = parser.parse_pdf(pdf_url)
    print("Parsing completed!")

    print()
    print(result[0].text_resource.text)
