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
    p_bom = load_processed_data(f'{PROCESSED_DATA_FILE_PATH}/pf-bom.pkl')
    name_dic = named_entity_recognition(p_bom, nlp, types=['PERSON'])
    print(name_dic['Jesus Christ'])

if __name__ == '__main__':
    start_time = dt.datetime.now()
    main()
    end_time = dt.datetime.now()
    print(f'Processing completed at {end_time} in {end_time - start_time}')