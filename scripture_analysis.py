import json, spacy, pickle, datetime as dt
from scripture_processing import *

nlp = spacy.load('en_core_web_lg')
nlp.max_length = 2000000
DATA_FILE_PATH = 'data'
PROCESSED_DATA_FILE_PATH = f'{DATA_FILE_PATH}/processed'
SCRIPTURE_DATA_FILE_PATH = f'{DATA_FILE_PATH}/scripture'
OUTPUT_FILE_PATH = 'output'

def named_entity_recognition():
    name_dic = []
    data = load_data("data/scriptures/flat/bom.json")
    processed_data = process_data(data)

    for doc in processed_data:
        for ent in doc.ents:
            if ent.label_ in ['PERSON', 'ORG', 'GPE']:
                if name_dic[ent.text] is None:
                    name_dic[ent.text] = 1
                name_dic[ent.text] += 1

def main():
    file_names = ['bom', 'dnc', 'nt', 'ot', 'pogp']
    preprocess_flat(nlp, file_names, PROCESSED_DATA_FILE_PATH)

if __name__ == '__main__':
    main()
    print(f'Processing completed at {dt.datetime.now()}')