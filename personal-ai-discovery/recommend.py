from openai import OpenAI

client = OpenAI()

# Load the persistent reader profile
with open("user_profile.txt", "r", encoding="utf-8") as file:
    profile = file.read()

prompt = f"""
You are recommending books to a reader based on the following
persistent taste profile.

--- READER PROFILE ---

{profile}

--- END PROFILE ---

Find five novels this reader might enjoy.

Use web search to look beyond the most obvious recommendations.
Consider older books, less famous authors, specialist publications,
reader discussions, and books that may have relatively little
mainstream attention.

Do NOT simply search for "books similar to" famous books. Instead,
search for books matching the specific combination of preferences in
the reader profile.

For each recommendation:
1. Explain which specific preferences make it a potential match.
2. Identify the most significant potential mismatch or reason the
   reader might dislike it.
3. Give a confidence rating from 1–10.
4. Do not recommend a book merely because it belongs to a genre the
   reader likes.

Include at least one genuinely less-obvious recommendation if you can
find one that is actually a strong fit.

Prioritize recommendation quality over obscurity.
"""

response = client.responses.create(
    model="gpt-6-luna",
    tools=[
        {
            "type": "web_search"
        }
    ],
    input=prompt
)

print(response.output_text)