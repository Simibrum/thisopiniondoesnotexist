"""Functions and variables for post generation."""


summarise_prompt = f"""/
Summarize this biography in 10 key words or phrase or less:

{{}}
"""

plan_prompt = f"""/
Write a outline plan for an online newspaper opinion article based on the information below. Set out the headings 
and sub-headings and write keyword notes on each paragraph contents. The full article will be around 1000 words long. 
Only write the outline plan for now.

Author is {{}}. Keywords for {{}}.

The date is {{}}.

The following are the topics for the opinion article: {{}}.

In the plan sketch out how you would tie the topics together. Write from the perspective of the author. 

Use the format:

Article Title: xxxx
Article Subheading: xxxx
Introduction: [key points]
Paragraph 1: [key points]
Paragraph 2: [key points]
etc.
Conclusion: [key points]
"""

# We need to pick 3 trending topic ourselves randomly to reduce the article size

#Use the schema: 1. Introduction, 2. Main Body, 3. Conclusion
paragraph_prompt = f"""/
You are {{}} {{}}. Keywords for {{}}.

Here is a plan for the article.

{{}}

Now start by writing {{}} from the plan. Don't include any headings:
"""