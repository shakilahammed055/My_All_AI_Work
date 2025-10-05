import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


def sytempromptchatbot(prompt: str) -> str:
    """Send a prompt along with the system prompt and return the assistant reply.

    This function signature matches how routes call it (sytempromptchatbot(prompt)).
    """
    system_prompt = (
        "You are MedInfo BD, an AI assistant specialized in providing factual information about medicines available in Bangladesh. "
        "Your responses must ONLY cover: (1) General details on medicines (e.g., generic name, common brand names, indications, dosage guidelines from DGDA or WHO, side effects, and precautions); "
        "(2) Current prices of medicines in Bangladesh (based on DGDA's official price list for 117 essential generics, or average market prices from sources like MedEx or Lazz Pharma; note recent hikes of 30-75% due to raw material costs and inflation—e.g., many generics cost Tk 1-50 per unit, but NCD drugs like insulin may exceed Tk 500). "
        "Always cite sources like DGDA.gov.bd, MedEx.com.bd, or recent studies (e.g., WHO/HAI surveys showing median price ratios of 0.33-2.56 for essentials). "
        "Do NOT provide personal medical advice, diagnoses, treatment recommendations, or discuss topics outside medicines in Bangladesh (e.g., no global comparisons, lifestyle tips, or unrelated health queries). "
        "If a query is off-topic, politely redirect: 'I can only assist with medicine information and prices in Bangladesh. Please consult a doctor for advice.' "
        "Respond in Bengali if the user asks in Bengali, otherwise in English. Keep responses concise, factual, and structured (e.g., use bullet points for details and prices). "
        "Latest data as of 2025: Prices are regulated by DGDA for essentials; check dgda.gov.bd/search-price for updates. Availability is ~70-80% in private pharmacies but lower in public facilities."
    )

    messages = [{"role": "system", "content": system_prompt}]

    # Retry-once for transient upstream rate-limits (HTTP 429).
    max_retries = 3
    backoff = 0.5
    completion = None
    for attempt in range(1, max_retries + 1):
        try:
            completion = client.chat.completions.create(
                model="deepseek/deepseek-chat-v3-0324:free",
                messages=messages + [{"role": "user", "content": prompt}],
            )
            break
        except Exception as exc:
            msg = str(exc)
            is_rate_limit = (
                "429" in msg
                or "rate-limit" in msg.lower()
                or "rate limited" in msg.lower()
                or "temporarily rate-limited" in msg.lower()
            )
            if is_rate_limit and attempt < max_retries:
                # transient; wait and retry with exponential backoff
                time.sleep(backoff)
                backoff *= 2
                continue
            # not retryable or out of retries
            raise RuntimeError(f"system prompt chat request failed: {exc}") from exc

    # Parse response
    try:
        msg = completion.choices[0].message.content
        return msg
    except Exception:
        # fallback to str(completion)
        try:
            return str(completion)
        except Exception:
            raise RuntimeError("unable to parse completion response")


if __name__ == "__main__":
    # Usage: First get the response function, then call it with a prompt
    get_response = sytempromptchatbot()
    msg = get_response("What is the price of Paracetamol in Bangladesh?")
    print(msg)
