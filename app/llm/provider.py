from typing import Type

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
)

from langchain_groq import ChatGroq

from app.config import (
    LLM_MODEL,
    GROQ_MODEL,
)


def get_gemini_llm():

    return ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        temperature=0,
    )


def get_groq_llm():

    return ChatGroq(
        model=GROQ_MODEL,
        temperature=0,
    )


def is_rate_limit_error(
    exception: Exception,
) -> bool:

    message = str(exception).lower()

    indicators = [
        "429",
        "resource_exhausted",
        "quota",
        "rate limit",
        "rate_limit",
        "too many requests",
    ]

    return any(
        indicator in message
        for indicator in indicators
    )


def invoke_with_fallback(
    prompt: str,
    output_schema: Type,
):

    # --------------------------------
    # Primary provider: Gemini
    # --------------------------------

    gemini = (
        get_gemini_llm()
        .with_structured_output(
            output_schema
        )
    )

    try:

        print(
            "\nLLM Provider: Gemini"
        )

        result = gemini.invoke(
            prompt
        )

        if result is None:
            raise ValueError(
                "Gemini returned None."
            )

        return result

    except Exception as gemini_error:

        if not is_rate_limit_error(
            gemini_error
        ):
            raise

        print(
            "\nGemini quota/rate limit reached."
        )

        print(
            "Switching to Groq..."
        )

    # --------------------------------
    # Fallback provider: Groq
    # --------------------------------

    groq = (
        get_groq_llm()
        .with_structured_output(
            output_schema
        )
    )

    try:

        print(
            f"\nLLM Provider: Groq "
            f"({GROQ_MODEL})"
        )

        result = groq.invoke(
            prompt
        )

        if result is None:
            raise ValueError(
                "Groq returned None."
            )

        return result

    except Exception as groq_error:

        print(
            "\nGroq fallback failed."
        )

        raise RuntimeError(
            "All configured LLM providers "
            "are currently unavailable."
        ) from groq_error