# IIT Madras Data Science 

An LLM-based API that helps answer questions from IIT Madras' Online Degree in Data Science course assignments.

## Features

- Accepts questions from any of the 5 graded assignments
- Handles file uploads (CSV and ZIP files)
- Returns answers in the correct format for assignment submission
- Deployed on Vercel for easy access

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/iitm-assignment-helper.git
cd iitm-assignment-helper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

4. Run the application locally:
```bash
python main.py
```

The API will be available at `http://localhost:8000/api/`

## API Usage

Send a POST request to the API endpoint with the following parameters:

- `question`: The assignment question (required)
- `file`: Optional file upload (CSV or ZIP containing CSV)

Example using curl:
```bash
curl -X POST "https://your-app.vercel.app/api/" \
  -H "Content-Type: multipart/form-data" \
  -F "question=Download and unzip file abcd.zip which has a single extract.csv file inside. What is the value in the 'answer' column of the CSV file?" \
  -F "file=@abcd.zip"
```

The API will return a JSON response in the following format:
```json
{
  "answer": "1234567890"
}
```

## Deployment

This application is configured for deployment on Vercel. To deploy:

1. Push your code to GitHub
2. Connect your repository to Vercel
3. Add your environment variables in the Vercel dashboard
4. Deploy!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 
