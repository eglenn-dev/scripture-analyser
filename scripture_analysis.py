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
    print('1. Book Most Popular Names in a Book (NER)')
    print('2. Which Book References Jesus Christ the Most? (NER)')
    print('3. Exit Program')
    user_input = input('Enter the number of the option you would like to run: ')
    if user_input == '1':
        ner()
    elif user_input == '2':
        jesus_references()
    elif user_input == '3':
        print('Exiting program...')
    else:
        print('Invalid option entered, exiting program...')

def jesus_references():
    os.system('cls' if os.name == 'nt' else 'clear')
    book_names = ['bom', 'dnc', 'nt', 'ot', 'pogp']
    if not check_processed_existence(PROCESSED_DATA_FILE_PATH, [f'pf-{book}.pkl' for book in book_names]):
        preprocess_flat_json(nlp, book_names, PROCESSED_DATA_FILE_PATH)
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Program Loaded Successfully!')
    types = ['PERSON', 'NORP']
    names = ['jesus', 'christ', 'jesus christ', 'messiah', 'lord', 'son of god', 'son of man', 'savior', 'saviour', 'redeemer', 'the word', 'god', 'the lamb', 'lamb of god', 'only begotten', 'god of israel', 'king of kings', 'lord of lords', 'alpha and omega', 'the beginning and the end', 'the first and the last', 'the light of the world', 'the way the truth and the life', 'the good shepherd', 'the true vine', 'the bread of life', 'the prince of peace', 'the holy one of israel']
    book_dic = {}
    print('Doing the calculations live, please wait...')
    for book in book_names:
        processed_book = load_processed_data(f'{PROCESSED_DATA_FILE_PATH}/pf-{book}.pkl')
        name_dic = named_entity_recognition(processed_book, types=types)
        book_dic[book] = 0
        for name in name_dic:
            if name.lower() in names:
                book_dic[book] += name_dic[name]

    book_dic = {k: v for k, v in sorted(book_dic.items(), key=lambda item: item[1], reverse=True)}
    for key, value in book_dic.items():
        print(f'{key.upper()}: {value}')

def ner():
    os.system('cls' if os.name == 'nt' else 'clear')
    book_names = ['bom', 'dnc', 'nt', 'ot', 'pogp']
    if not check_processed_existence(PROCESSED_DATA_FILE_PATH, [f'pf-{book}.pkl' for book in book_names]):
        preprocess_flat_json(nlp, book_names, PROCESSED_DATA_FILE_PATH)
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
    processed_book = load_processed_data(f'{PROCESSED_DATA_FILE_PATH}/pf-{user_book}.pkl')
    name_dic = named_entity_recognition(processed_book, types=['PERSON'])
    print(f'Top 10 Names in {user_book.upper()}:')
    for name in sorted(name_dic, key=name_dic.get, reverse=True)[:10]:
        print(f'{name}: {name_dic[name]}')

if __name__ == '__main__':
    main()