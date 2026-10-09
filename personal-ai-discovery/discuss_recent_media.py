from openai import OpenAI
from datetime import datetime

client = OpenAI()

with open("user_profile.txt", "r", encoding="utf-8") as file:
    profile = file.read()

print("Let's talk about something you recently finished.")
print("Type 'quit' at any time to stop.\n")

media = input("What did you recently read, watch, play, or otherwise experience?\n\nYou: ")

if media.lower() == "quit":
    print("\nConversation ended.")
    exit()

print("\nDo you have a few minutes to talk about it?\n")

ready = input("You: ")

if ready.lower() == "quit":
    print("\nConversation ended.")
    exit()

conversation = []
conversation.append("AI: What did you recently read, watch, play, or otherwise experience?")
conversation.append("You: " + media)
conversation.append("AI: Do you have a few minutes to talk about it?")
conversation.append("You: " + ready)


# ---------------------------------------------------------
# Start the conversation.
# ---------------------------------------------------------

prompt = f"""
You are having a relaxed, thoughtful conversation with a reader about
something they recently experienced.

The reader's current taste profile is:

--- PROFILE ---
{profile}
--- END PROFILE ---

The reader recently experienced:

--- MEDIA ---
{media}
--- END MEDIA ---

Here is the conversation so far:

{conversation}

The reader has indicated that they have time to talk.

Your goal is to have an enjoyable, natural conversation about the
media with them, much like a thoughtful friend discussing something
they both know.

This conversation is NOT primarily an interview and NOT a survey.

Do not try to systematically extract information about the reader's
preferences.

Do not ask questions merely because the answers might improve the
reader's profile. Their conversation will be analyzed separately later.

Instead:

- Talk about the media itself.
- Respond thoughtfully to what the reader says.
- Follow subjects they seem genuinely interested in.
- Ask questions when a question would naturally advance the discussion.
- Offer observations about the work when useful.
- Remember things the reader has already said during the conversation.
- If the reader raises an interesting interpretation, explore it with
  them.
- If they criticize something, engage with the criticism rather than
  simply asking them to elaborate.
- If they praise something, explore what makes it work.
- You may gently disagree or offer another interpretation when that
  would make the discussion more interesting, but do not argue merely
  for the sake of arguing.
- Do not reflexively agree with everything the reader says.
- Do not constantly ask "How did that make you feel?" or otherwise
  turn the discussion into a psychological interview.
- Do not force the discussion toward topics already present in the
  profile.
- If the reader changes subjects, follow them.

The conversation should feel socially natural.

There is no required number of questions or turns. Let the discussion
develop naturally.

If the reader gives a short answer, respond appropriately rather than
forcing a long discussion.

If the reader indicates that they are finished, respond with a brief,
natural closing remark and do not ask another question.

Do not mention profiles, data collection, recommendation systems,
analysis, or any behind-the-scenes purpose.

Your goal is simply to have an interesting conversation about the
media the reader just experienced.
"""

while True:

    response = client.responses.create(
        model="gpt-6-luna",
        input=prompt
    )

    ai_message = response.output_text.strip()

    print("\nAI:", ai_message)

    conversation.append("AI: " + ai_message)

    answer = input("\nYou: ")

    if answer.lower() == "quit":
        break

    conversation.append("You: " + answer)

    prompt = f"""
You are continuing a relaxed, thoughtful conversation with a reader
about something they recently experienced.

The reader's current taste profile is:

--- PROFILE ---
{profile}
--- END PROFILE ---

The media being discussed is:

--- MEDIA ---
{media}
--- END MEDIA ---

Here is the conversation so far:

{conversation}

Continue the conversation naturally.

This is a social discussion, not an interview or questionnaire.

Respond primarily to what the reader JUST SAID.

Talk about the media itself and follow the direction of the
conversation.

You may:
- make an observation
- respond to an interpretation
- discuss something interesting in the work
- gently disagree or offer another interpretation
- ask a natural follow-up question
- connect two things the reader has already said
- explore something the reader seems interested in

Do not ask questions merely to collect preference information.

Do not force the conversation toward subjects in the profile.

Do not repeatedly ask the reader to explain their feelings.

Do not simply agree with everything they say.

Let the conversation breathe. A response does not always need to end
with a question.

If the reader indicates that they are finished, give one brief,
natural closing remark and do not ask another question.

Do not mention profiles, data collection, recommendation systems,
analysis, or any behind-the-scenes purpose.

The goal is to have an enjoyable conversation with the reader about
the media they just experienced.
"""

print("\nConversation ended.")

# ---------------------------------------------------------
# Save the completed conversation.
# ---------------------------------------------------------

if conversation:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"conversations/discuss_recent_media_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as file:
        for line in conversation:
            file.write(line + "\n\n")

    print("Conversation saved to:", filename)