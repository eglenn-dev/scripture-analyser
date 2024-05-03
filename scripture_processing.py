import json, pickle, os

def load_json_data(filepath):
    with open(filepath) as f:
        data = json.load(f)
    return data.get('verses', [])

def save_processed_data(processed_data, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(processed_data, f)

def load_processed_data(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

def save_json_data(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f)

def process_data(data, nlp):
    all_text = " ".join([item['text'] for item in data])
    docs = []
    for i in range(0, len(all_text), 1000000):
        doc = nlp(all_text[i:i+1000000])
        docs.append(doc)
    return docs

def check_processed_existence(directory, files):
    dir_files = os.listdir(directory)
    if len(dir_files) != len(files):
        return False
    for file in dir_files:
        if file not in files:
            return False
    return True

def preprocess_flat_json(nlp, file_names, processed_data_file_path):
    if not os.path.exists(processed_data_file_path):
        os.makedirs(processed_data_file_path)
    try:
        print('Attempting to load processed data...')
        for file in file_names:
            load_processed_data(f'{processed_data_file_path}/pf-{file}.pkl')
        print('Processed data loaded successfully')
    except:
        print('Error loading data, processing data again...')
        for file in file_names:
            data = load_json_data(f'data/scriptures/flat/{file}.json')
            docs = process_data(data, nlp)
            save_processed_data(docs, f'{processed_data_file_path}/pf-{file}.pkl')
        print('Data processed successfully')

def named_entity_recognition(processed_data, types=[]):
    name_dic = {}
    for doc in processed_data:
        for ent in doc.ents:
            if ent.label_ in types:
                if ent.text not in name_dic:
                    name_dic[ent.text] = 1
                else:
                    name_dic[ent.text] += 1
    return name_dic

def get_named_entities(processed_data, types=[]):
    entities = []
    for doc in processed_data:
        for ent in doc.ents:
            if ent.label_ in types:
                entities.append(ent.text)
    return entities
