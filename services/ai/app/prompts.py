SYSTEM_PROMPT = """You are an operations diagnosis assistant. Use only the supplied
context, distinguish evidence from hypotheses, and suggest safe verification steps.
Never claim an automated action was executed."""


def build_prompt(question: str, context: list[str]) -> str:
    joined = "\n\n".join(context) if context else "No matching internal context."
    return f"{SYSTEM_PROMPT}\n\nContext:\n{joined}\n\nQuestion:\n{question}"
