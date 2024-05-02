import spacy

nlp = spacy.load("en_core_web_lg")  # Load a spaCy model

# Get the named entity recognition (NER) component
ner = nlp.get_pipe('ner')

# Access the supported labels as a set
labels = ner.labels

# Print all the labels
print(labels)
