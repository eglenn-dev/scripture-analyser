import json, spacy, pickle, datetime as dt
from scripture_processing import *

nlp = spacy.load('en_core_web_lg')
nlp.max_length = 2000000
DATA_FILE_PATH = 'data'
PROCESSED_DATA_FILE_PATH = f'{DATA_FILE_PATH}/processed'
SCRIPTURE_DATA_FILE_PATH = f'{DATA_FILE_PATH}/scriptures'
OUTPUT_FILE_PATH = 'output'

def main():
    file_names = ['bom', 'dnc', 'nt', 'ot', 'pogp']
    preprocess_flat(nlp, file_names, PROCESSED_DATA_FILE_PATH)
    bom = load_data(f'{SCRIPTURE_DATA_FILE_PATH}/flat/bom.json')
    name_dic = named_entity_recognition(bom, nlp, types=['PERSON', 'ORG', 'GPE'])
    print(name_dic['Christ'])

if __name__ == '__main__':
    main()
    print(f'Processing completed at {dt.datetime.now()}')