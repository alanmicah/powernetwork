import spacy

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

# Process whole documents

import json
reportsJson = open('data/live_reports.json', 'r')
eachReports = json.load(reportsJson)

text=""

for items in eachReports:
  for line in items:
      if isinstance(line,str):
        text+='"'+ line+' "'

# Find named entities, phrases and concepts

print(text)
doc=nlp(text)
for entity in doc.ents:
                print(entity.text, entity.label_)
# # Analyze syntax
# print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
# print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

# # Find named entities, phrases and concepts
# for entity in doc.ents:
#     print(entity.text, entity.label_)