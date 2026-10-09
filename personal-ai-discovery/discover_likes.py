from openai import OpenAI
from datetime import datetime

client = OpenAI()

with open("user_profile.txt", "r", encoding="utf-8") as file:
    profile = file.read()

print("Let's talk about something you enjoy.")
print("Type 'quit' when you want to stop.\n")

conversation = []
answer_count = 0

while True:
    if not conversation:
        prompt = f"""
You are having a brief, casual conversation with a reader about
something they enjoy.

Here is what you already know about the reader:

--- PROFILE ---
{profile}
--- END PROFILE ---

Your job is to have a pleasant, natural conversation with this person.

This is a QUICK CHECK-IN. Assume they may only have a minute or two.
Do not turn the interaction into an interview or questionnaire.

Start with an open-ended question about something the reader has been
enjoying recently.

The reader's answers will be analyzed separately later to determine
whether they contain useful information about their long-term tastes.
You do NOT need to identify or extract those preferences yourself.

Your goal is simply to be an engaging conversational partner who knows
something about the reader.
"""

    else:
        prompt = f"""
You are having a brief, casual conversation with a reader about
something they enjoy.

Here is what you already know about the reader:

--- PROFILE ---
{profile}
--- END PROFILE ---

Here is the conversation so far:

{conversation}

Your job is to have a pleasant, natural conversation with this person.

This is a QUICK CHECK-IN. Assume they may only have a minute or two.
Do not turn the interaction into an interview or questionnaire.

Respond primarily to what the reader JUST SAID.

If they mention a book, movie, game, author, idea, character, or other
subject, engage with that subject rather than immediately trying to
extract information about their tastes.

You may:
- react to what they said
- make an observation
- connect it to something you already know about them
- express curiosity
- ask a natural follow-up question

Do not ask a question merely because it could provide useful profile
information.

Do not force the conversation toward speculative fiction, books, or
any other particular category just because those subjects appear in
the profile.

If the reader changes subjects, follow them.

Keep the interaction brief unless the reader clearly indicates that
they want to continue.

If the reader gives a short answer, keep your response short.

The reader's answers will be analyzed separately later to determine
whether they contain useful information about their long-term tastes.
You do NOT need to identify or extract those preferences yourself.

Your goal is simply to be an engaging conversational partner who knows
something about the reader.
"""

    response = client.responses.create(
        model="gpt-6-luna",
        input=prompt
    )

    question = response.output_text.strip()

    print("AI:", question)

    answer = input("\nYou: ")

    if answer.lower() == "quit":
        break

    answer_count += 1

    conversation.append("AI: " + question)
    conversation.append("You: " + answer)

    if answer_count >= 2:
        closing_prompt = f"""
You are ending a very brief, casual conversation with a reader.

Here is the conversation:

{conversation}

The reader has just given their second answer, so this interaction is
now over.

Respond with one brief, warm, natural closing remark acknowledging what
the reader just said.

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

        conversation.append("AI: " + closing)
        break

print("\nConversation ended.")

# Save the completed conversation.
if conversation:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"conversations/discover_likes_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as file:
        for line in conversation:
            file.write(line + "\n\n")

    print("Conversation saved to:", filename)