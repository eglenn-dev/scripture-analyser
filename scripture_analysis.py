import spacy, os, datetime as dt
from scripture_processing import *

nlp = spacy.load('en_core_web_lg')
nlp.max_length = 4000000
DATA_FILE_PATH = 'data'
PROCESSED_LIST_DATA_FILE_PATH = f'{DATA_FILE_PATH}/processed/list'
PROCESSED_NLP_DATA_FILE_PATH = f'{DATA_FILE_PATH}/processed/nlp'
SCRIPTURE_DATA_FILE_PATH = f'{DATA_FILE_PATH}/scriptures'
OUTPUT_FILE_PATH = f'{DATA_FILE_PATH}/output'

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Scripture Analysis Program')
    print('1. Book Most Popular Names in a Book (NER)')
    print('2. Which Book References Jesus Christ the Most? (NER)')
    print('3. Which book is most similar to another book? (NLP)')
    print('4. Exit Program')
    user_input = input('Enter the number of the option you would like to run: ')
    if user_input == '1':
        ner()
    elif user_input == '2':
        jesus_references()
    elif user_input == '3':
        book_similarity()
    elif user_input == '4':
        print('Exiting program...')
    else:
        print('Invalid option entered, exiting program...')

def jesus_references():
    os.system('cls' if os.name == 'nt' else 'clear')
    book_names = ['bom', 'dnc', 'nt', 'ot', 'pogp']
    if not check_processed_existence(PROCESSED_LIST_DATA_FILE_PATH, [f'pf-{book}.pkl' for book in book_names]):
        preprocess_json(nlp, book_names, PROCESSED_LIST_DATA_FILE_PATH)
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Program Loaded Successfully!')
    types = ['PERSON', 'NORP']
    names = ['jesus', 'christ', 'jesus christ', 'messiah', 'lord', 'son of god', 'son of man', 'savior', 'saviour', 'redeemer', 'the word', 'god', 'the lamb', 'lamb of god', 'only begotten', 'god of israel', 'king of kings', 'lord of lords', 'alpha and omega', 'the beginning and the end', 'the first and the last', 'the light of the world', 'the way the truth and the life', 'the good shepherd', 'the true vine', 'the bread of life', 'the prince of peace', 'the holy one of israel']
    book_dic = {}
    print('Doing the calculations live, please wait...')
    for book in book_names:
        processed_book = load_processed_data(f'{PROCESSED_LIST_DATA_FILE_PATH}/pf-{book}.pkl')
        name_dic = named_entity_recognition(processed_book, types=types)
        book_dic[book] = 0
        for name in name_dic:
            if name.lower() in names:
                book_dic[book] += name_dic[name]
    book_dic = {k: v for k, v in sorted(book_dic.items(), key=lambda item: item[1], reverse=True)}
    save_json_data(book_dic, f'{OUTPUT_FILE_PATH}/jesus_references.json')
    print(f'\nReferences to Jesus Christ by Book: ')
    for key, value in book_dic.items():
        print(f'{key.upper()}: {value}')

def ner():
    os.system('cls' if os.name == 'nt' else 'clear')
    book_names = ['bom', 'dnc', 'nt', 'ot', 'pogp']
    if not check_processed_existence(PROCESSED_LIST_DATA_FILE_PATH, [f'pf-{book}.pkl' for book in book_names]):
        preprocess_json(nlp, book_names, PROCESSED_LIST_DATA_FILE_PATH)
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
    processed_book = load_processed_data(f'{PROCESSED_LIST_DATA_FILE_PATH}/pf-{user_book}.pkl')
    name_dic = named_entity_recognition(processed_book, types=['PERSON'])
    save_json_data(name_dic, f'{OUTPUT_FILE_PATH}/ner-{user_book}.json')
    print(f'Top 10 Names in {user_book.upper()}:')
    for name in sorted(name_dic, key=name_dic.get, reverse=True)[:10]:
        print(f'{name}: {name_dic[name]}')

def book_similarity():
    os.system('cls' if os.name == 'nt' else 'clear')
    book_names = ['bom', 'dnc', 'nt', 'ot', 'pogp']
    if not check_processed_existence(PROCESSED_NLP_DATA_FILE_PATH, [f'nlp-{book}.pkl' for book in book_names]):
        preprocess_nlp(nlp, book_names, PROCESSED_NLP_DATA_FILE_PATH)
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Program Loaded Successfully!')
    similarity_scores = {}
    for i in range(len(book_names)):
        book1 = book_names[i]
        processed_book1 = load_processed_data(f'{PROCESSED_NLP_DATA_FILE_PATH}/nlp-{book1}.pkl')
        for j in range(i + 1, len(book_names)):
            book2 = book_names[j]
            processed_book2 = load_processed_data(f'{PROCESSED_NLP_DATA_FILE_PATH}/nlp-{book2}.pkl')
            similarity_scores[f'{book1};{book2}'] = processed_book1.similarity(processed_book2)
    similarity_scores = {k: v for k, v in sorted(similarity_scores.items(), key=lambda item: item[1], reverse=True)}
    save_score_data(similarity_scores, f'{OUTPUT_FILE_PATH}/book_similarity_scores.json')
    print(f'\nBook Similarity Scores: ')
    for key, value in similarity_scores.items():
        print(f'{key.upper()}: {value}')

if __name__ == '__main__':
    main()