import spacy, os, datetime as dt
from scripture_processing import *

nlp = spacy.load('en_core_web_lg')
nlp.max_length = 2000000
DATA_FILE_PATH = 'data'
PROCESSED_DATA_FILE_PATH = f'{DATA_FILE_PATH}/processed'
SCRIPTURE_DATA_FILE_PATH = f'{DATA_FILE_PATH}/scriptures'
OUTPUT_FILE_PATH = 'output'

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    book_names = ['bom', 'dnc', 'nt', 'ot', 'pogp']
    if not check_processed_existence(PROCESSED_DATA_FILE_PATH, [f'pf-{book}.pkl' for book in book_names]):
        preprocess_flat(nlp, book_names, PROCESSED_DATA_FILE_PATH)
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Program Loaded Successfully!')
    print('Book Options:')
    for i, book in enumerate(book_names):
        print(f'{i+1}. {book.upper()}')
    user_book = input('Enter the book you would like to analyze: ').lower()
    if user_book not in book_names:
        print('Invalid book name entered, exiting program...')
        return
    processed_book = load_processed_data(f'{PROCESSED_DATA_FILE_PATH}/pf-{user_book}.pkl')
    name_dic = named_entity_recognition(processed_book, nlp, types=['PERSON'])
    print('Top 10 Names:')
    for name in sorted(name_dic, key=name_dic.get, reverse=True)[:10]:
        print(f'{name}: {name_dic[name]}')

if __name__ == '__main__':
    start_time = dt.datetime.now()
    main()
    end_time = dt.datetime.now()
    print(f'Program completed at {end_time} in {end_time - start_time}')