from app.models import ConversationState


def extract_state(messages):

    combined_text = " ".join(
        msg["content"].lower()
        for msg in messages
        if msg["role"] == "user"
    )

    # role detection

    role = None

    role_keywords = [
        "engineer",
        "developer",
        "manager",
        "analyst",
        "designer",
        "leader",
        "architect",
        "software engineer",
        "software developer",
        "graduate engineer"
    ]

    for keyword in role_keywords:

        if keyword in combined_text:
            role = keyword.title()
            break

    # seniority

    seniority = None

    if any(word in combined_text for word in [
        "entry",
        "junior",
        "fresher",
        "graduate"
    ]):
        seniority = "Entry-Level"

    elif any(word in combined_text for word in [
        "mid",
        "mid-level"
    ]):
        seniority = "Mid-Professional"

    elif any(word in combined_text for word in [
        "senior",
        "lead"
    ]):
        seniority = "Senior"

    # skills

    known_skills = [
        "java",
        "python",
        "javascript",
        "react",
        "node",
        "backend",
        "frontend",
        "aws",
        "sql",
        "cloud",
        "api",
        "software"
    ]

    skills = []

    for skill in known_skills:

        if skill in combined_text:
            skills.append(skill)

    # assessment signals

    needs_technical = any(word in combined_text for word in [
        "technical",
        "coding",
        "developer",
        "engineer",
        "programming",
        "backend",
        "frontend",
        "software engineer",
        "software developer",
        "java",
        "python",
        "javascript",
        "graduate engineer"
    ])

    needs_personality = any(word in combined_text for word in [
        "personality",
        "behavior",
        "culture",
        "soft skills",
        "leadership",
        "communication",
        "stakeholder",
        "manager"
    ])

    needs_cognitive = any(word in combined_text for word in [
        "aptitude",
        "cognitive",
        "reasoning",
        "iq",
        "analytical"
    ])

    communication_required = any(word in combined_text for word in [
        "communication",
        "stakeholder",
        "client-facing"
    ])

    leadership_required = any(word in combined_text for word in [
        "leadership",
        "leader",
        "manager",
        "management",
        "lead team"
    ])

    # recommendation readiness

    ready_for_recommendation = any([
        role,
        skills,
        leadership_required,
        communication_required,
        needs_technical,
        needs_personality,
        needs_cognitive
    ])

    # if role + seniority known, recommend directly
    if role and seniority:
        ready_for_recommendation = True

    # leadership hiring shouldn't require tech stack
    if leadership_required:
        ready_for_recommendation = True

    # graduate technical hiring should work
    if (
        seniority == "Entry-Level"
        and needs_technical
    ):
        ready_for_recommendation = True

    return ConversationState(
        role=role,
        seniority=seniority,
        skills=skills,
        needs_technical=needs_technical,
        needs_personality=needs_personality,
        needs_cognitive=needs_cognitive,
        communication_required=communication_required,
        leadership_required=leadership_required,
        ready_for_recommendation=ready_for_recommendation
    )