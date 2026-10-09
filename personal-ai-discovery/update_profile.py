from openai import OpenAI
import os
from datetime import datetime
import shutil

client = OpenAI()

conversation_folder = "conversations"
processed_file = "processed_conversations.txt"


# ---------------------------------------------------------
# Load the current profile.
# ---------------------------------------------------------

with open("user_profile.txt", "r", encoding="utf-8") as file:
    profile = file.read()


# ---------------------------------------------------------
# Load the list of conversations that have already been
# incorporated into the profile.
# ---------------------------------------------------------

if os.path.exists(processed_file):
    with open(processed_file, "r", encoding="utf-8") as file:
        processed_conversations = {
            line.strip()
            for line in file
            if line.strip()
        }
else:
    processed_conversations = set()


# ---------------------------------------------------------
# Find all saved conversations.
# ---------------------------------------------------------

conversation_files = [
    file for file in os.listdir(conversation_folder)
    if file.endswith(".txt")
]


if not conversation_files:
    print("No saved conversations found.")
    exit()


# ---------------------------------------------------------
# Keep only conversations that have not been processed yet.
# ---------------------------------------------------------

unprocessed_files = [
    file for file in conversation_files
    if file not in processed_conversations
]


if not unprocessed_files:
    print("No new conversations to analyze.")
    exit()


# ---------------------------------------------------------
# Process conversations chronologically.
#
# The timestamp is part of the filename, so alphabetical
# sorting gives us chronological order.
# ---------------------------------------------------------

unprocessed_files.sort()


print("Found", len(unprocessed_files), "new conversation(s).")


# ---------------------------------------------------------
# Process each conversation.
# ---------------------------------------------------------

for filename in unprocessed_files:

    conversation_path = os.path.join(
        conversation_folder,
        filename
    )

    with open(conversation_path, "r", encoding="utf-8") as file:
        conversation = file.read()

    print("\n========================================")
    print("Analyzing:", filename)
    print("========================================")


    # -----------------------------------------------------
    # Analyze the conversation.
    # -----------------------------------------------------

    analysis_prompt = f"""
You are analyzing a short conversation with a reader in order to
determine whether it contains useful information about their
long-term tastes.

The reader already has the following persistent taste profile:

--- CURRENT PROFILE ---
{profile}
--- END CURRENT PROFILE ---

Here is the new conversation:

--- CONVERSATION ---
{conversation}
--- END CONVERSATION ---

Analyze the conversation carefully.

Your job is NOT to rewrite the profile yet. Instead, report what useful
information, if any, the conversation provides.

Separate your findings into these categories:

1. EXPLICIT PREFERENCES
Things the reader directly said they like, dislike, value, or care about.

2. POSSIBLE DURABLE PREFERENCES
Things that may represent a broader preference, but where the evidence
is not yet strong enough to treat them as certain.

3. PROFILE REFINEMENTS
Ways the new conversation might usefully clarify, narrow, broaden, or
qualify something already present in the profile.

4. CONTRADICTIONS
Anything in the conversation that appears to conflict with the current
profile.

5. THINGS NOT TO INFER
Important conclusions that might be tempting to draw from the
conversation but are not actually supported strongly enough.

Be conservative.

Do not treat merely mentioning a book, movie, game, author, genre, or
subject as evidence that the reader likes it.

Do not infer a general preference from a single example unless the
reader clearly expresses a general preference.

Distinguish between:
- "I like this particular work."
- "I like this particular aspect of this work."
- "I generally like this kind of thing."

Pay attention to the strength of the reader's language.

Do not assume that a preference is universal simply because the reader
responded positively to something.

The purpose of this analysis is to provide high-quality evidence for a
future persistent taste profile, not to maximize the number of
preferences discovered.

If a category has nothing useful to report, say "None."
"""


    analysis_response = client.responses.create(
        model="gpt-6-luna",
        input=analysis_prompt
    )

    analysis = analysis_response.output_text.strip()


    print("\n--- ANALYSIS ---\n")
    print(analysis)


    # -----------------------------------------------------
    # Create the revised profile.
    # -----------------------------------------------------

    profile_prompt = f"""
You maintain a concise, persistent profile describing a reader's
tastes.

Here is the reader's current profile:

--- CURRENT PROFILE ---
{profile}
--- END CURRENT PROFILE ---

Here is a new conversation with the reader:

--- CONVERSATION ---
{conversation}
--- END CONVERSATION ---

Here is an analysis of what the conversation may tell us:

--- ANALYSIS ---
{analysis}
--- END ANALYSIS ---

Create a proposed revised version of the reader's taste profile.

IMPORTANT RULES:

1. Preserve useful information already present in the profile.

2. Do not rewrite the profile merely to make it sound different.

3. Add a new preference only when the evidence supports it.

4. Prefer refining an existing preference over creating a redundant
   new preference.

5. Do not turn a preference for one particular work into a general
   preference unless the reader clearly indicates that it is general.

6. Distinguish strong preferences from tentative ones.

7. If the new conversation qualifies or narrows an existing preference,
   modify the existing statement rather than simply adding another
   contradictory statement.

8. If the reader explicitly contradicts something in the existing
   profile, revise that part of the profile rather than ignoring the
   contradiction.

9. Do not include individual book titles merely as a list of things the
   reader has read. Include them only when they provide useful evidence
   for a broader preference.

10. Do not include unsupported speculation.

11. Keep the profile concise. It should describe the reader's durable
    tastes, not their entire reading history.

12. The profile should describe preferences rather than facts about the
    reader.

Return ONLY the proposed revised profile. Do not include an introduction,
explanation, analysis, or commentary.
"""


    profile_response = client.responses.create(
        model="gpt-6-luna",
        input=profile_prompt
    )

    proposed_profile = profile_response.output_text.strip()


    print("\n--- PROPOSED PROFILE ---\n")
    print(proposed_profile)


    # -----------------------------------------------------
    # Back up the current profile before replacing it.
    # -----------------------------------------------------

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    backup_filename = f"user_profile_{timestamp}.txt"

    backup_path = os.path.join(
        "profile_backups",
        backup_filename
    )

    shutil.copy2(
        "user_profile.txt",
        backup_path
    )

    print("\nCurrent profile backed up to:", backup_path)


    # -----------------------------------------------------
    # Replace the current profile.
    # -----------------------------------------------------

    with open("user_profile.txt", "w", encoding="utf-8") as file:
        file.write(proposed_profile)

    print("Updated user_profile.txt")


    # -----------------------------------------------------
    # Update our processing ledger.
    #
    # We only record the conversation AFTER its profile
    # update has successfully completed.
    # -----------------------------------------------------

    with open(processed_file, "a", encoding="utf-8") as file:
        file.write(filename + "\n")

    print("Recorded as processed:", filename)


    # -----------------------------------------------------
    # The newly updated profile becomes the starting point
    # for the next conversation.
    # -----------------------------------------------------

    profile = proposed_profile


print("\n========================================")
print("Profile update complete.")
print("Processed", len(unprocessed_files), "conversation(s).")
print("========================================")