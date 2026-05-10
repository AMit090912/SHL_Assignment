from collections import defaultdict


def retrieve_assessments(state, catalog):

    scored = []

    user_query = " ".join(state.skills).lower()

    if state.role:
        user_query += " " + state.role.lower()

    if state.seniority:
        user_query += " " + state.seniority.lower()

    for item in catalog:

        score = 0

        combined_text = (
            item.name + " " +
            " ".join(item.categories)
        ).lower()

        # technical matching
        if state.needs_technical:

            # exact skill match
            for skill in state.skills:

                if skill.lower() in combined_text:
                    score += 8

            # technical keywords
            technical_keywords = [
                "java",
                "python",
                "javascript",
                "developer",
                "backend",
                "frontend",
                "programming",
                "cloud",
                "aws",
                "api",
                "automata"
            ]

            for keyword in technical_keywords:

                if keyword in combined_text:
                    score += 3

            # boost automata for technical hiring
            if "automata" in combined_text:
                score += 2

        # personality matching
        if state.needs_personality:

            personality_keywords = [
                "personality",
                "behavior",
                "opq",
                "leadership",
                "team",
                "culture",
                "competencies"
            ]

            if any(
                keyword in combined_text
                for keyword in personality_keywords
            ):
                score += 5

            # prefer generic OPQ reports
            if "opq32r" in combined_text:
                score += 6

            # avoid sales-heavy reports
            if (
                "sales" in combined_text
                and "sales" not in user_query
            ):
                score -= 15

        # cognitive / aptitude
        if state.needs_cognitive:

            cognitive_keywords = [
                "aptitude",
                "ability",
                "reasoning",
                "verify",
                "numerical",
                "deductive",
                "inductive",
                "cognitive"
            ]

            if any(
                keyword in combined_text
                for keyword in cognitive_keywords
            ):
                score += 6

        # leadership
        if state.leadership_required:

            leadership_keywords = [
                "leadership",
                "manager",
                "management",
                "executive",
                "team"
            ]

            if any(
                keyword in combined_text
                for keyword in leadership_keywords
            ):
                score += 6

            # avoid sales-heavy leadership reports
            if (
                "sales" in combined_text
                and "sales" not in user_query
            ):
                score -= 15

        # communication
        if state.communication_required:

            communication_keywords = [
                "communication",
                "customer",
                "stakeholder",
                "service",
                "team"
            ]

            if any(
                keyword in combined_text
                for keyword in communication_keywords
            ):
                score += 4

        # entry-level boost
        if state.seniority == "Entry-Level":

            # junior technical assessments
            if any(
                keyword in combined_text
                for keyword in [
                    "junior",
                    "graduate",
                    "foundation"
                ]
            ):
                score += 4

            # only boost "entry" if technical too
            if (
                "entry" in combined_text
                and any(
                    skill in combined_text
                    for skill in state.skills
                )
            ):
                score += 2

        # senior-level boost
        if state.seniority == "Senior":

            if any(
                keyword in combined_text
                for keyword in [
                    "senior",
                    "leadership",
                    "manager",
                    "executive"
                ]
            ):
                score += 4

        # ignore weak matches
        if score < 2:
            continue

        scored.append((score, item))

    # sort by score
    scored.sort(
        key=lambda x: x[0],
        reverse=True
    )

    results = [item for score, item in scored]
    

    final_results = []

    has_personality = False
    has_cognitive = False

    # keep top technical matches first
    for item in results[:7]:
        final_results.append(item)

    # add one personality assessment
    for item in results:

        category_text = " ".join(item.categories).lower()

        if (
            not has_personality
            and any(
                word in category_text
                for word in [
                    "personality",
                    "behavior"
                ]
            )
        ):
            final_results.append(item)
            has_personality = True
            break

    # add one aptitude assessment
    for item in results:

        category_text = " ".join(item.categories).lower()

        if (
            not has_cognitive
            and any(
                word in category_text
                for word in [
                    "ability",
                    "aptitude"
                ]
            )
        ):
            final_results.append(item)
            has_cognitive = True
            break

    # remove duplicates
    unique_results = []
    seen = set()

    for item in final_results:

        if item.url in seen:
            continue

        seen.add(item.url)
        unique_results.append(item)

    return unique_results[:10]

