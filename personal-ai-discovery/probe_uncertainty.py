from openai import OpenAI
from datetime import datetime

client = OpenAI()

with open("user_profile.txt", "r", encoding="utf-8") as file:
    profile = file.read()

print("Let's clarify something about your tastes.")
print("Type 'quit' if you don't want to answer.\n")


# ---------------------------------------------------------
# Ask the AI to identify one useful uncertainty in the
# current profile.
# ---------------------------------------------------------

probe_prompt = f"""
You are helping maintain a persistent taste profile for a reader.

Here is the reader's current profile:

--- PROFILE ---
{profile}
--- END PROFILE ---

Your task is to identify ONE meaningful uncertainty, ambiguity, or
poorly understood area in this profile that could be clarified by
asking the reader a single natural question.

Look for things such as:

- preferences that are currently too broad
- apparent exceptions that may reveal an important qualification
- areas where two pieces of evidence seem difficult to reconcile
- preferences whose boundaries are unclear
- distinctions that would meaningfully improve future recommendations

Do NOT ask about something merely because the profile lacks information
about it.

Do NOT try to fill every possible gap in the profile.

Do NOT ask about a specific fact such as a favorite author, favorite
book, or favorite genre unless knowing that fact would actually clarify
a broader preference.

Choose the single uncertainty whose clarification would be most useful
for understanding the reader's tastes.

Then formulate ONE natural, conversational question that would help
clarify it.

The question should:
- sound like something a thoughtful friend might ask
- be understandable without explaining the profile to the reader
- avoid mentioning "profile," "data," "analysis," or recommendation
  systems
- not feel like a survey question
- give the reader room to explain their reasoning
- avoid leading the reader toward a particular answer

Return ONLY the question.
"""

probe_response = client.responses.create(
    model="gpt-6-luna",
    input=probe_prompt
)

question = probe_response.output_text.strip()

print("AI:", question)

answer = input("\nYou: ")

if answer.lower() == "quit":
    print("\nConversation ended.")
    exit()


# ---------------------------------------------------------
# Give the reader a brief closing remark.
# ---------------------------------------------------------

closing_prompt = f"""
You are ending a very brief conversation with a reader.

The question was:

{question}

The reader answered:

{answer}

Respond with one brief, natural closing remark acknowledging their
answer.

Do NOT ask another question.
Do NOT introduce a new subject.
Do NOT mention profiles, preferences, data collection, or analysis.
Do NOT make the response unnecessarily formal.

The goal is simply to make the conversation feel naturally finished.
"""

closing_response = client.responses.create(
    model="gpt-6-luna",
    input=closing_prompt
)

closing = closing_response.output_text.strip()

print("\nAI:", closing)


# ---------------------------------------------------------
# Save the conversation.
# ---------------------------------------------------------

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"conversations/probe_uncertainty_{timestamp}.txt"

with open(filename, "w", encoding="utf-8") as file:
    file.write("AI: " + question + "\n\n")
    file.write("You: " + answer + "\n\n")
    file.write("AI: " + closing + "\n\n")

print("\nConversation saved to:", filename)