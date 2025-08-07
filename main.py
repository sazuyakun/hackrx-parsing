from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from parser.PDFParser import PDFParser
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

uri = os.getenv("MONGO_URI")
client = MongoClient(uri, server_api=ServerApi('1'))

load_dotenv()

LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")

app = FastAPI(title="PDF to Markdown Converter", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to connect to MongoDB")

    # Connect to DB collection
    db = client["llama_docs"]
    collection = db["parsed_pdfs"]

    pdf_url = (
        "https://hackrx.blob.core.windows.net/assets/Arogya%20Sanjeevani%20Policy%20"
        "-%20CIN%20-%20U10200WB1906GOI001713%201.pdf"
        "?sv=2023-01-03&st=2025-07-21T08%3A29%3A02Z"
        "&se=2025-09-22T08%3A29%3A00Z&sr=b&sp=r"
        "&sig=nzrz1K9Iurt%2BBXom%2FB%2BMPTFMFP3PRnIvEsipAX10Ig4%3D"
    )

    # Check if result already in DB
    existing = collection.find_one({"url": pdf_url})
    if existing:
        print("Fetched from DB")
        return JSONResponse(
            content={
                "message": "Fetched from database!",
                "text": existing["parsed"][0]  # first page
            }
        )

    # Parse using LlamaParse
    parser = PDFParser(api_key=LLAMA_CLOUD_API_KEY)
    result = parser.parse_pdf(pdf_url)
    parsed_text = [doc.text for doc in result]

    # Store in MongoDB
    collection.insert_one({"url": pdf_url, "parsed": parsed_text})
    print("Parsing completed and stored in DB!")

    return JSONResponse(
        content={
            "message": "Parsed and stored!",
            "text": parsed_text[0]  # first page
        }
    )


# Example usage
# if __name__ == "__main__":
#     parser = PDFParser(api_key=LLAMA_CLOUD_API_KEY)

#     pdf_url = "https://hackrx.blob.core.windows.net/assets/Arogya%20Sanjeevani%20Policy%20-%20CIN%20-%20U10200WB1906GOI001713%201.pdf?sv=2023-01-03&st=2025-07-21T08%3A29%3A02Z&se=2025-09-22T08%3A29%3A00Z&sr=b&sp=r&sig=nzrz1K9Iurt%2BBXom%2FB%2BMPTFMFP3PRnIvEsipAX10Ig4%3D"

#     result = parser.parse_pdf(pdf_url)
#     print("Parsing completed!")

#     print()
#     print(result[0].text_resource.text)