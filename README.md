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
