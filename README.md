# Trade Opportunities API

A production-style FastAPI service that analyzes Indian market sectors and returns a markdown report of trade opportunities using web search and Gemini AI.

## Features

- **Sector market analysis**: Analyzes dynamic market sectors.
- **AI insights using Gemini**: Leverages Google's generative AI to find insights and opportunities.
- **Markdown report generation**: Returns a clean and parsed markdown string.
- **Authentication**: Secured with simple API Key headers.
- **Rate limiting**: Restricts identical IP addresses to prevent abuse (SlowAPI).
- **Session tracking**: In-memory IP logging and stats.

## Setup Instructions

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Environment Variables:**
Create a `.env` file in the project root:

```ini
GEMINI_API_KEY=your_api_key_here
API_SECRET_KEY=appscrip-secret-key
```

3. **Run server:**

```bash
uvicorn app.main:app --reload
```

## API Endpoint
`GET /analyze/{sector}`

Fetch an analysis report for a specific string. 

**Example:**
`/analyze/pharmaceuticals`

**Headers:**
`x-api-key: appscrip-secret-key`

## Built With
- FastAPI
- DuckDuckGo Search
- Google Generative AI (Gemini)
- SlowAPI
- Pydantic
