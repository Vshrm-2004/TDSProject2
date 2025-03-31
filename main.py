from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
import tempfile
import zipfile
from typing import Optional
import openai
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="IIT Madras Data Science Assignment Helper")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

def process_csv_file(file_path: str) -> str:
    """Process CSV file and return the value in the 'answer' column."""
    try:
        df = pd.read_csv(file_path)
        if 'answer' in df.columns:
            return str(df['answer'].iloc[0])
        return "No 'answer' column found in the CSV file."
    except Exception as e:
        return f"Error processing CSV file: {str(e)}"

def extract_zip_file(zip_path: str) -> Optional[str]:
    """Extract ZIP file and return the path to the CSV file."""
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
                for file in os.listdir(temp_dir):
                    if file.endswith('.csv'):
                        return os.path.join(temp_dir, file)
        return None
    except Exception as e:
        print(f"Error extracting ZIP file: {str(e)}")
        return None

@app.post("/api/")
async def answer_question(
    question: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    """
    Endpoint to answer questions from IIT Madras Data Science assignments.
    Accepts a question and optional file upload.
    """
    try:
        # If a file is uploaded, process it first
        file_content = None
        if file:
            # Save the uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                content = await file.read()
                temp_file.write(content)
                temp_file_path = temp_file.name

            # Process based on file type
            if file.filename.endswith('.zip'):
                csv_path = extract_zip_file(temp_file_path)
                if csv_path:
                    file_content = process_csv_file(csv_path)
            elif file.filename.endswith('.csv'):
                file_content = process_csv_file(temp_file_path)

            # Clean up
            os.unlink(temp_file_path)

        # Prepare the prompt for the LLM
        prompt = f"""You are an expert in Data Science and a student at IIT Madras. 
        Please answer the following question from the IIT Madras Data Science course assignment.
        If a file was provided, here is its content: {file_content}
        
        Question: {question}
        
        Please provide a clear, concise answer that can be directly entered into the assignment.
        Focus on accuracy and ensure the answer is in the correct format."""

        # Get response from OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant specialized in answering IIT Madras Data Science course questions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )

        answer = response.choices[0].message.content.strip()
        
        return {"answer": answer}

    except Exception as e:
        return {"answer": f"Error processing request: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 