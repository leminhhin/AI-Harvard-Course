import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    result = dict()
    for file in os.listdir(directory):
        with open(os.path.join(directory, file), "r") as f:
            result[file] = f.read()
    return result
    # raise NotImplementedError

def isValid(word):
    return word not in string.punctuation and word not in nltk.corpus.stopwords.words("english")

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    document = nltk.word_tokenize(document)
    document = [word for word in document if isValid(word)]
    return document
    # raise NotImplementedError

def is_exist(word, document):
    return word in document

def count_documents(documents):
    """
    Given a dictionary of `documents`, return a dictionary that maps words to their number of documents containing them.
    """
    result = dict()
    words = set()

    # get all words
    for document in documents:
        words.update(documents[document])

    # count documents
    for word in words:
        count = 0
        for document in documents:
            if is_exist(word, documents[document]):
                count+=1
        result[word] = count
    return result

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    result = dict()
    count_docs = count_documents(documents)
    n = len(documents)

    for word in count_docs:
        result[word] = math.log(n/count_docs[word])

    return result
    # raise NotImplementedError

def term_frequency(word, document):
    frq = 0
    for w in document:
        if w == word:
            frq += 1
    return frq

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    file_score = dict()
    for file in files:
        score = 0
        for word in query:
            if word in files[file]:
                tf = term_frequency(word, files[file])
                idf = idfs[word]
                score += tf*idf
        file_score[file] = score
    return sorted(file_score, key=file_score.get, reverse=True)[:n]
    # raise NotImplementedError

def query_term_density(query, sentence):
    sentence = set(sentence)
    return len(query&sentence) / len(sentence)

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_score = dict()
    for sen in sentences:
        idf = 0
        for word in query:
            if word in sentences[sen]:
                idf += idfs[word]
        density = query_term_density(query, sentences[sen])
        sentence_score[sen] = (idf, density)

    return sorted(sentence_score, key=lambda x: (sentence_score[x][0],sentence_score[x][1]), reverse=True)[:3]

    # raise NotImplementedError


if __name__ == "__main__":
    main()
