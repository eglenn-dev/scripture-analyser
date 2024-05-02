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
    print('Scripture Analysis Program')
    print('1. Named Entity Recognition')
    print('3. Exit Program')
    user_input = input('Enter the number of the option you would like to run: ')
    if user_input == '1':
        ner()
    elif user_input == '3':
        print('Exiting program...')
    else:
        print('Invalid option entered, exiting program...')

def ner():
    os.system('cls' if os.name == 'nt' else 'clear')
    book_names = ['bom', 'dnc', 'nt', 'ot', 'pogp']
    if not check_processed_existence(f'{PROCESSED_DATA_FILE_PATH}/ner', [f'pf-{book}.pkl' for book in book_names]):
        preprocess_flat_json(nlp, book_names, f'{PROCESSED_DATA_FILE_PATH}/ner')
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Program Loaded Successfully!')
    print('Book Options:')
    for i, book in enumerate(book_names):
        print(f'{i+1}. {book.upper()}')
    user_book = input('Enter the book you would like to analyze: ').lower()
    if (user_book not in book_names) and (user_book not in [str(i+1) for i in range(len(book_names))]):
        print('Invalid book name entered, exiting program...')
        return
    if user_book in [str(i+1) for i in range(len(book_names))]:
        user_book = book_names[int(user_book)-1]
    processed_book = load_processed_data(f'{PROCESSED_DATA_FILE_PATH}/ner/pf-{user_book}.pkl')
    name_dic = named_entity_recognition(processed_book, nlp, types=['PERSON'])
    print('Top 10 Names:')
    for name in sorted(name_dic, key=name_dic.get, reverse=True)[:10]:
        print(f'{name}: {name_dic[name]}')

if __name__ == '__main__':
    main()