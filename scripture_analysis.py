# Library and Module imports
import spacy, os, datetime as dt
from scripture_processing import *

# Global Variables
nlp = spacy.load('en_core_web_lg')
nlp.max_length = 4000000
DATA_FILE_PATH = 'data'
PROCESSED_LIST_DATA_FILE_PATH = f'{DATA_FILE_PATH}/processed/list'
PROCESSED_NLP_DATA_FILE_PATH = f'{DATA_FILE_PATH}/processed/nlp'
SCRIPTURE_DATA_FILE_PATH = f'{DATA_FILE_PATH}/scriptures'
OUTPUT_FILE_PATH = f'{DATA_FILE_PATH}/output'

# Main Function
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Scripture Analysis Program')
    print('1. Book Most Popular Names in a Book (NER)')
    print('2. Which Book References Jesus Christ the Most? (NER)')
    print('3. Which book is most similar to another book? (NLP)')
    print('4. Which verse is most similar to another? (NLP)')
    print('5. Exit Program')

    # User Input
    user_input = input('Enter the number of the option you would like to run: ')

    # Running the corresponding function based on the user input
    if user_input == '1':
        ner()
    elif user_input == '2':
        jesus_references()
    elif user_input == '3':
        book_similarity()
    elif user_input == '4':
        compare_verses()
    elif user_input == '5':
        print('Exiting program...')
    else:
        print('Invalid option entered, exiting program...')

def jesus_references():
    """
    This function calculates the number of references to Jesus Christ in different books.
    The books are specified by their names in the 'book_names' list.
    The function uses Named Entity Recognition (NER) to identify references to Jesus Christ.
    The references are identified by a list of names/titles for Jesus Christ.
    The function saves the results to a JSON file and also prints them to the console.

    The function performs the following steps:
    1. Clears the console.
    2. Checks if the processed data for the books exist. If not, preprocesses the JSON data.
    3. Clears the console again and prints a success message.
    4. Defines the entity types and names to look for in the NER.
    5. Initializes an empty dictionary to hold the results.
    6. For each book, loads the processed data and performs NER.
    7. Counts the occurrences of each name in the book and adds the count to the results.
    8. Sorts the results by the count of references in descending order.
    9. Saves the results to a JSON file.
    10. Prints the results to the console.

    Parameters:
    None

    Returns:
    None
    """
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
    """
    This function performs Named Entity Recognition (NER) on a selected book.
    The books are specified by their names in the 'book_names' list.
    The function uses the 'PERSON' entity type to identify names in the book.
    The function saves the results to a JSON file and also prints the top 10 names to the console.

    The function performs the following steps:
    1. Clears the console.
    2. Checks if the processed data for the books exist. If not, preprocesses the JSON data.
    3. Clears the console again and prints a success message.
    4. Prints the list of book options.
    5. Asks the user to enter the name of the book they would like to analyze.
    6. If the user enters an invalid book name, the function prints an error message and returns.
    7. If the user enters a valid book name, the function loads the processed data for the book.
    8. Performs NER on the processed data to identify names ('PERSON' entities).
    9. Saves the results to a JSON file.
    10. Prints the top 10 names in the book to the console.

    Parameters: None

    Returns:
    None
    """
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
    """
    This function calculates the similarity scores between different books.
    The books are specified by their names in the 'book_names' list.
    The function uses the spaCy language model's similarity method to calculate the similarity between each pair of books.
    The function saves the results to a JSON file and also prints them to the console.

    The function performs the following steps:
    1. Clears the console.
    2. Checks if the processed data for the books exist. If not, preprocesses the data.
    3. Clears the console again and prints a success message.
    4. Initializes an empty dictionary to hold the results.
    5. For each pair of books, loads the processed data and calculates the similarity score.
    6. Stores the similarity score in the results dictionary.
    7. Sorts the results by the similarity score in descending order.
    8. Saves the results to a JSON file.
    9. Prints the results to the console.

    Parameters: None

    Returns:
    None
    """
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

def compare_verses():
    """
    This function allows the user to select a book and a specific verse from that book to find similar verses across the same book.
    The similarity is calculated using the spaCy NLP model's similarity method on the processed text data of the verses.
    The function performs the following steps:
    1. Clears the console.
    2. Displays a list of book options to the user.
    3. Prompts the user to select a book by entering the book name or the corresponding number.
    4. If the user enters an invalid book name or number, the function prints an error message and exits.
    5. Prompts the user to enter the verse they would like to compare.
    6. Loads the processed data for the selected book.
    7. Calculates the similarity scores between the selected verse and all other verses in the book.
    8. Sorts the verses by their similarity scores in descending order.
    9. Prints the most similar verses to the console, including their references and similarity scores.

    Parameters:
    None

    Returns:
    None
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    book_names = ['bom', 'dnc', 'nt', 'ot', 'pogp']
    for i, book in enumerate(book_names):
        print(f'{i+1}. {book.upper()}')
    user_book = input('Enter the book you would like to compare: ')
    if (user_book not in book_names) and (user_book not in [str(i+1) for i in range(len(book_names))]):
        print('Invalid book name entered, exiting program...')
        return
    if user_book in [str(i+1) for i in range(len(book_names))]:
        user_book = book_names[int(user_book)-1]
    user_verse = input(f'Enter the verse you would like to compare from {user_book.upper()}: ')
    print(f'Selected verse is: {user_verse}')
    print("Loading data dictionary...")
    book_dic = create_dictionary(read_json_file(f'{SCRIPTURE_DATA_FILE_PATH}/flat/{user_book}.json'))
    print('Comparing verses...')
    similar_verses = find_similar_verses(nlp, user_verse, book_dic)
    print(f'\nMost Similar Verses to {user_verse}:')
    for reference, similarity in similar_verses:
        print(f'Reference: {reference}')
        print(f'Verse: {book_dic[reference]}')
        print(f'Similarity: {similarity:.2f}')

if __name__ == '__main__':
    main()