# AI Interview Coach

An AI-powered interview preparation platform that helps candidates assess their job readiness, practice personalized interview questions, and improve their interview performance through structured, AI-generated feedback.

## Overview

AI Interview Coach leverages Google Gemini and Streamlit to analyze candidate resumes against job descriptions, identify relevant skills and skill gaps, generate role-specific interview questions, and evaluate candidate responses.

The platform aims to make interview preparation more structured, personalized, and accessible.

## Key Features

- **Resume Analysis:** Extracts and analyzes candidate information from PDF resumes.
- **Job Description Matching:** Evaluates the alignment between a candidate's profile and the requirements of a target role.
- **Personalized Interview Questions:** Generates technical, project-based, behavioral, and skill-gap-related questions.
- **Answer Evaluation:** Assesses responses based on relevance, depth, clarity, and supporting examples.
- **Performance Feedback:** Identifies strengths and areas requiring improvement.
- **Personalized Study Plan:** Provides recommendations to help candidates prepare more effectively for interviews.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and backend processing |
| Streamlit | Interactive web interface |
| Google Gemini API | AI-powered analysis, question generation, and evaluation |
| PyPDF | PDF resume text extraction |
| python-dotenv | Local environment variable management |

## Project Structure

```text
AI-Interview-Coach/
├── app.py
├── coach.py
├── Llm.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

Follow these steps to run the project locally.

### Prerequisites

- Python 3.11 or later
- Git
- A Google Gemini API key

### 1. Clone the Repository

```bash
git clone https://github.com/deepak-bhee/AI-Interview-Coach.git
cd AI-Interview-Coach
```

### 2. Create a Virtual Environment

```bash
python3 -m venv coach_env
```

Activate the environment on macOS or Linux:

```bash
source coach_env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Obtain an API key through [Google AI Studio](https://aistudio.google.com/).

**Security note:** Never commit your `.env` file or expose your API key in public repositories.

### 5. Run the Application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, typically:

`http://localhost:8501`

## Application Workflow

1. **Upload Resume:** Provide a resume in PDF format.
2. **Enter Job Description:** Specify the target position's requirements.
3. **Analyze Profile:** Review the profile match score, relevant skills, and identified skill gaps.
4. **Generate Questions:** Receive personalized interview questions based on the candidate's profile and target role.
5. **Complete the Interview:** Submit responses to the generated questions.
6. **Review Evaluation:** Examine feedback on answer quality, strengths, and improvement areas.
7. **Follow the Study Plan:** Use the recommendations to guide further preparation.

## Deployment

The application can be deployed using Streamlit Community Cloud.

1. Push the project repository to GitHub.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Connect the GitHub repository.
4. Select `app.py` as the main application file.
5. Configure `GEMINI_API_KEY` in the application's Streamlit Secrets settings.
6. Deploy the application.

The application must be configured to read the API key from Streamlit Secrets in the deployed environment.

## Future Enhancements

- Voice-based mock interview simulations
- Speech recognition and communication analysis
- Candidate interview history and progress tracking
- Expanded support for document formats
- Detailed performance reports and analytics
- Role-specific interview preparation pathways

## Security and Privacy

- API credentials should be stored securely and excluded from version control.
- Uploaded resumes may contain personal information. Handle candidate data responsibly.
- Avoid retaining or logging sensitive candidate information unnecessarily.

## Author

**Deepak**  
Computer Science and Engineering

## License

No license has been specified yet. Unless a license is added, reuse and redistribution are subject to the default applicable copyright rules.
