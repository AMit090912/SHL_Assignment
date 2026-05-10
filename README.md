# SHL Assessment Recommendation Agent

A conversational recommendation agent built for the SHL assessment catalog.  
The system helps recruiters and hiring teams discover relevant SHL assessments based on hiring requirements through a stateless FastAPI API.

The agent supports:
- Clarifying vague hiring requests
- Recommending SHL assessments
- Refining recommendations during conversation
- Comparing assessments
- Refusing off-topic and prompt-injection requests

---

# Features

## Clarification Handling
The agent asks follow-up questions when the user query is too vague.

Example:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Need hiring assessments"
    }
  ]
}

## Assessment Recommendations
The agent recommends between 1 and 10 SHL assessments using catalog-grounded retrieval.

Example:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hiring a Java backend developer with stakeholder communication"
    }
  ]
}
```


## Refinement Support
The agent supports conversational refinement.

Example:

```text
Actually add personality assessments
```

---

## Comparison Support
The agent can compare assessments when requested.

Example:

```text
What is the difference between OPQ and GSA?
```

---

## Safety & Scope Control
The agent:
- Only discusses SHL assessments
- Refuses off-topic questions
- Refuses prompt injection attempts
- Returns only catalog-grounded URLs

---

# Tech Stack

- Python
- FastAPI
- Pydantic
- Rule-based retrieval and scoring

---

# Project Structure

```text
project/
│
├── app/
│   ├── agent.py
│   ├── catalog_loader.py
│   ├── main.py
│   ├── models.py
│   ├── retriever.py
│   └── state_extractor.py
│
├── data/
│   └── shl_catalog.json
│
├── requirements.txt
├── README.md
```

---

# API Endpoints

## Root Endpoint

```http
GET /
```

Response:

```json
{
  "message": "SHL Assessment Recommendation API"
}
```

---

## Health Check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

---

## Chat Endpoint

```http
POST /chat
```

Request Body:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hiring a Java backend developer"
    }
  ]
}
```

Example Response:

```json
{
  "reply": "Here are some SHL assessments that match your hiring requirements.",
  "recommendations": [
    {
      "name": "Core Java (Advanced Level) (New)",
      "url": "https://www.shl.com/products/product-catalog/view/core-java-advanced-level-new/",
      "test_type": "Knowledge & Skills"
    }
  ],
  "end_of_conversation": true
}
```

---

# Retrieval Approach

The system uses a grounded retrieval approach built on top of the SHL catalog.

The retrieval pipeline:
1. Extracts conversational state from user messages
2. Detects:
   - Role
   - Seniority
   - Skills
   - Technical requirements
   - Personality requirements
   - Leadership requirements
3. Scores catalog assessments using keyword and category matching
4. Ranks and filters the best matching assessments

The system prioritizes:
- Technical skill relevance
- Personality and leadership alignment
- Cognitive assessment signals
- Communication requirements

---

# Running Locally

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run FastAPI server

```bash
uvicorn app.main:app --reload
```

---

# Deployment

Deployed on Render:

https://shl-assignment-7r1q.onrender.com

Swagger Docs:

https://shl-assignment-7r1q.onrender.com/docs

---

# Example Supported Queries

## Technical Hiring

```text
Hiring a Java backend developer with stakeholder communication
```

## Leadership Hiring

```text
Need leadership and communication assessments for managers
```

## Graduate Hiring

```text
Need assessments for graduate software engineers
```

## Comparison Query

```text
What is the difference between OPQ and GSA?
```

---

# Notes

- The API is stateless.
- All recommendations are grounded in the SHL catalog.
- All returned URLs come directly from the catalog data.
- The system avoids hallucinated recommendations.
