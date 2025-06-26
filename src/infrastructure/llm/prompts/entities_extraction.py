ENTITY_EXTRACTION_PROMPT = """
You are an expert HR assistant. Extract structured data from the provided resume text.
Return the result in JSON with the following fields:
- name, email, phone (number, remove all the non-numeric characters except +)
- summary (short summary of the candidate)
- education (list of: institution, degree, field, start_date, end_date)
- skills (list)
- work_experience: list(years_of_experience (integer) + company + positions (title) + description): Return the total years of experience in each specific position. If empty, return 0 with the position title and other attributes is None.
- total_work_experience (integer): Total years of work experience.
- certifications (list of: title, date, description): Relevant certifications.
- achievements (list of: title, date): Honours, awards, publications, etc.

<Constraint>
- Only rely on the provided resume text.
- If the text contains broken words, line breaks, or spelling mistakes, correct them and merge split words.
- Rewrite the summary and other text fields fluently and naturally in English.
- Do not make assumptions but you can infer information from the text and rewrite it more fluent.
- Return in valid JSON format.
- Summarize the projects and papers in a concise manner. Keep all the statistics and dates.
- Only include the fields mentioned above.
- work_experience_for_embedding must at least return 0 with the position title and other attributes as None if no work experience is found.
- Do not include any additional information or explanations.
- You can extract information from projects, certifications and rewrite them as skills with descriptions. Only extract the skills not the title of those.
- Always return every field in the JSON with approriate field types even if they are empty.
</Constraint>
Resume text:
"""