import json, pickle, os

def load_json_data(filepath):
    with open(filepath) as f:
        data = json.load(f)
    return data.get('verses', [])

def read_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

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

def process_data_nlp(data, nlp):
    all_text = " ".join([item['text'] for item in data])
    doc = nlp(all_text)
    return doc

def save_score_data(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f)

def check_processed_existence(directory, files):
    dir_files = os.listdir(directory)
    if len(dir_files) != len(files):
        return False
    for file in dir_files:
        if file not in files:
            return False
    return True

def preprocess_nlp(nlp, file_names, processed_data_file_path):
    if not os.path.exists(processed_data_file_path):
        os.makedirs(processed_data_file_path)
    for file in file_names:
        try:
            print('Attempting to load processed data...')
            load_processed_data(f'{processed_data_file_path}/nlp-{file}.pkl')
            print('Processed data loaded successfully')
        except:
            print('Error loading data, processing data again...')
            data = load_json_data(f'data/scriptures/flat/{file}.json')
            docs = process_data_nlp(data, nlp)
            save_processed_data(docs, f'{processed_data_file_path}/nlp-{file}.pkl')
    print('Data processed successfully')

def preprocess_json(nlp, file_names, processed_data_file_path):
    if not os.path.exists(processed_data_file_path):
        os.makedirs(processed_data_file_path)
    for file in file_names:
        try:
            print('Attempting to load processed data...')
            load_processed_data(f'{processed_data_file_path}/pf-{file}.pkl')
            print('Processed data loaded successfully')
        except:
            print('Error loading data, processing data again...')
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

def compare_verses(nlp, doc1, verse2):
    doc2 = nlp(verse2)
    return doc1.similarity(doc2)

def find_similar_verses(nlp, target_verse, data_dict):
    similar_verses = []
    doc1 = nlp(data_dict[target_verse])
    for reference, verse in data_dict.items():
        if reference != target_verse:
            similarity = compare_verses(nlp, doc1, verse)
            similar_verses.append((reference, similarity))
        
    similar_verses.sort(key=lambda x: x[1], reverse=True)
    return similar_verses[:3]  

def create_dictionary(json_data):
    new_dict = {}
    for item in json_data.get('verses', []):
        new_dict[item['reference']] = item['text']
    return new_dict
