from app.models import (
    ChatResponse,
    Recommendation
)

from app.state_extractor import extract_state
from app.retriever import retrieve_assessments

INJECTION_PATTERNS = [
    "ignore previous instructions",
    "disregard instructions",
    "forget previous instructions",
    "bypass",
    "override system",
    "recommend certifications",
    "recommend coursera",
    "recommend udemy"
]

OFF_TOPIC_KEYWORDS = [
    "salary",
    "weather",
    "movie",
    "sports",
    "politics",
    "recipe",
    "ipl",
    "cricket",
    "football",
    "basketball"
]
def is_prompt_injection(messages):

    combined = " ".join(
        msg["content"].lower()
        for msg in messages
        if msg["role"] == "user"
    )

    return any(
        pattern in combined
        for pattern in INJECTION_PATTERNS
    )


def is_off_topic(messages):

    combined = " ".join(
        msg["content"].lower()
        for msg in messages
        if msg["role"] == "user"
    )

    return any(
        word in combined
        for word in OFF_TOPIC_KEYWORDS
    )


def build_agent_response(messages, catalog):
    combined = " ".join(
        msg["content"].lower()
        for msg in messages
        if msg["role"] == "user"
    )

        # comparison questions
    if (
        "difference between" in combined
        or "compare" in combined
    ):

        # OPQ vs GSA
        if "opq" in combined and "gsa" in combined:

            return ChatResponse(
                reply=(
                    "OPQ assessments focus on personality, behavior, "
                    "and workplace preferences, while GSA assessments "
                    "focus more on cognitive ability, reasoning, "
                    "and general skills evaluation."
                ),
                recommendations=[],
                end_of_conversation=True
            )

    if is_prompt_injection(messages):

        return ChatResponse(
            reply=(
                "I can only recommend "
                "assessments from the SHL catalog."
            ),
            recommendations=[],
            end_of_conversation=False
        )

    # Refuse off-topic
    if is_off_topic(messages):

        return ChatResponse(
            reply=(
                "I can only help with "
                "SHL assessment recommendations."
            ),
            recommendations=[],
            end_of_conversation=False
        )

    # Extract conversation state
    state = extract_state(messages)

    # Clarification logic
    if not state.ready_for_recommendation:

        missing_parts = []

        if not state.role:
            missing_parts.append("role")

        if not state.seniority:
            missing_parts.append("seniority level")

        if len(state.skills) == 0 and state.needs_technical:
            missing_parts.append("technical stack or skills")

        reply = (
            "Could you share the "
            + ", ".join(missing_parts)
            + "?"
        )

        return ChatResponse(
            reply=reply,
            recommendations=[],
            end_of_conversation=False
        )

    # Retrieve assessments
    results = retrieve_assessments(
        state,
        catalog
    )

    # No results
    if not results:

        return ChatResponse(
            reply=(
                "I could not find suitable "
                "SHL assessments for those "
                "requirements. Could you provide "
                "more details?"
            ),
            recommendations=[],
            end_of_conversation=False
        )

    # Build recommendations
    recommendations = []

    for item in results[:10]:

        category = (
            item.categories[0]
            if item.categories
            else "Assessment"
        )

        recommendations.append(
            Recommendation(
                name=item.name,
                url=item.url,
                test_type=category
            )
        )

    return ChatResponse(
        reply=(
            "Here are some SHL assessments "
            "that match your hiring requirements."
        ),
        recommendations=recommendations,
        end_of_conversation=True
    )