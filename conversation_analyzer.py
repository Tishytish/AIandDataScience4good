"""
Conversation Analyzer
======================
Input:  A conversation formatted as alternating Person A / Person B messages.
Output: JSON with 8 fields:
  1. last_message_original        - the last message in English
  2. last_message_rohingya        - Rohingya translation of the last message
  3. suggestion_1_english         - response suggestion 1 in English
  4. suggestion_1_rohingya        - suggestion 1 translated to Rohingya
  5. suggestion_2_english         - response suggestion 2 in English
  6. suggestion_2_rohingya        - suggestion 2 translated to Rohingya
  7. suggestion_3_english         - response suggestion 3 in English
  8. suggestion_3_rohingya        - suggestion 3 translated to Rohingya

Usage:
    python conversation_analyzer.py

    Or import and call analyze_conversation() directly in your own app:
        from conversation_analyzer import analyze_conversation
        result = analyze_conversation(my_conversation)
"""
import seckey
GEMINI_API_KEY = seckey.key
import os
import json
import anthropic
from google import genai

client = genai.Client(api_key=GEMINI_API_KEY)



# ── Sample conversation (replace with your real input) ────────────────────────

SAMPLE_CONVERSATION = [
    {"speaker": "Person A", "text": "Hey, did you manage to book the meeting room for Thursday?"},
    {"speaker": "Person B", "text": "Not yet, the system kept timing out when I tried yesterday."},
    {"speaker": "Person A", "text": "We really need it sorted — the client is flying in at 10am."},
    {"speaker": "Person B", "text": "I'll try again first thing tomorrow morning and let you know."},
    {"speaker": "Person A", "text": "Thanks. If it still doesn't work, just message me and I'll ask the office manager."},
]


# ── Core function ─────────────────────────────────────────────────────────────

def analyze_conversation(conversation: list[dict]) -> dict:
    """
    Takes a conversation as a list of { speaker, text } dicts.
    Returns a dict with 8 keys: last message + translation, and
    3 response suggestions each with their Rohingya translation.

    Args:
        conversation: [
            { "speaker": "Person A", "text": "Hello, how are you?" },
            { "speaker": "Person B", "text": "I'm good, thanks!" },
            ...
        ]

    Returns:
        {
            "last_message_original":  str,
            "last_message_rohingya":  str,
            "suggestion_1_english":   str,
            "suggestion_1_rohingya":  str,
            "suggestion_2_english":   str,
            "suggestion_2_rohingya":  str,
            "suggestion_3_english":   str,
            "suggestion_3_rohingya":  str,
        }
    """
    """
    if not ANTHROPIC_API_KEY:
        raise EnvironmentError("ANTHROPIC_API_KEY environment variable is not set.")

    if not conversation:
        raise ValueError("Conversation is empty.")
    """

   # client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    last_message = conversation[-1]
    conversation_text = "\n".join(f"{m['speaker']}: {m['text']}" for m in conversation)

    prompt = f"""You are a helpful assistant and expert translator.

Below is a conversation between two people:

{conversation_text}

The last message was sent by {last_message['speaker']}:
"{last_message['text']}"

Your tasks:
1. Translate the last message into Spanish. Use the Spanish script. 
2. Write 3 distinct suggested replies in English that the other person could send next. Each suggestion must have a meaningfully different tone: one professional, one casual, one empathetic.
3. Translate each of the 3 suggestions into Spanish (same script rules as above).

Return ONLY a valid JSON object with exactly these 8 keys. No preamble, no explanation, no markdown fences:

{{
  "last_message_original": "...",
  "last_message_spanish": "...",
  "suggestion_1_english": "...",
  "suggestion_1_spanish": "...",
  "suggestion_2_english": "...",
  "suggestion_2_spanish": "...",
  "suggestion_3_english": "...",
  "suggestion_3_spanish": "..."
}}"""

    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

    
    raw = response.text.strip()
    clean = raw.replace("```json", "").replace("```", "").strip()
    result2 = json.loads(clean)
    #output = json.dumps(result2, ensure_ascii=False, indent=2)
    return result2


# ── Pretty print helper ───────────────────────────────────────────────────────

def print_results(result: dict):
    divider = "─" * 60
    print(f"\n{divider}")
    print("LAST MESSAGE")
    print(divider)
    print(f"  English  : {result['last_message_original']}")
    print(f"  Spanish : {result['last_message_spanish']}")

    for i in range(1, 4):
        print(f"\n{divider}")
        print(f"SUGGESTION {i}")
        print(divider)
        print(f"  English  : {result[f'suggestion_{i}_english']}")
        print(f"  Spanish : {result[f'suggestion_{i}_spanish']}")

    print(f"\n{divider}\n")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Analyzing conversation...")

    result = analyze_conversation(SAMPLE_CONVERSATION)

    #print_results(result)

    print(result)
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)