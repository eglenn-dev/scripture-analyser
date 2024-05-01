import json, pickle

def load_data(filepath):
    with open(filepath) as f:
        data = json.load(f)
    return data.get('verses', [])

def save_processed_data(processed_data, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(processed_data, f)

def load_processed_data(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

def save_data(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f)

def process_data(data, nlp):
    all_text = " ".join([item['text'] for item in data])
    docs = []
    for i in range(0, len(all_text), 1000000):
        doc = nlp(all_text[i:i+1000000])
        docs.append(doc)
    return docs

def preprocess_flat(nlp, file_names, processed_data_file_path):
    for file in file_names:
        data = load_data(f'data/scriptures/flat/{file}.json')
        docs = process_data(data, nlp)
        save_processed_data(docs, f'{processed_data_file_path}/{file}.pkl')