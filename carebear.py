# encoding: utf-8
"""
Core methods
"""

import re
from textblob import TextBlob
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

punkt_parameters = PunktParameters()
punkt_parameters.abbrev_types = set(['al'])
tokeniser = PunktSentenceTokenizer(punkt_parameters)


# This should be improved, but is just a prototype
REGEX_LIST_LATEX = {
    # \citep; (Author et al. YYYY)
    '\citep{}': re.compile(
        r'\\citep\{(\w+)\}'
    ),
    # \citet; Author et al. (YYYY)
    '\citet{}': re.compile(
        r'\\citet\{(\w+)\}'
    ),
    # \citealt; Author et al. YYYY
    '\citealt{}': re.compile(
        r'\\citealt\{(\w+)\}'
    ),
}


REGEX_LIST_PDF = {
    # \citet
    'Author et al. (YYYY), '
    'Author (YYYY)': re.compile(
        r'\w+\s(?:et\sal\.\s)?\(\d+\)'
    ),
    # \citep
    '(Author et al. YYYY), '
    '(Author YYYY)': re.compile(
        r'\(\w+\s(?:et\sal.\s)?\d+\)'
    ),
}


def get_sentinment(text):
    """
    Return a number based on the sentiment of the text
    :param text: sentence that contains a citation
    :type text: str
    """
    return TextBlob(text).sentiment.polarity


def get_bbl_map(text):
    """
    From a BBL file create a map of citep name to reference
    :param text: content of a .bbl file
    :type text: str
    """
    regex_map = re.compile(
        r'\]\{(\w+)\}(.*)$'
    )

    bbl_map = {}

    for i in text.split('\\bibitem'):
        bbl = regex_map.search(i.replace('\n', ''))
        if bbl is not None and bbl.groups():
            group_two = bbl.group(2)
            group_two = group_two.replace('{', '')\
                                 .replace('}', '')\
                                 .replace('~', ' ')\
                                 .replace('\&', '&')\
                                 .replace('\endthebibliography', '')
            bbl_map[bbl.group(1)] = group_two

    return bbl_map


def get_sentences_latex(text):
    """
    Get all the sentences that have citations for any of the citation formatst
    that we recognise
    :param text: paragraph or full text latex document
    :type text: str
    """

    citation_sentences = {}
    sentences = tokeniser.tokenize(text)
    for sentence in sentences:
        for fmt, regex in REGEX_LIST_LATEX.items():
            search = [i for i in regex.findall(sentence) if i !='']
            if search:
                for s in search:
                    citation_sentences[s] = sentence
                break
    return citation_sentences


def get_sentences_pdf(text):
    """
    Get all the sentences that have citations for any of the formats that we
    recognise.

    :param text: paragraph or full document of text
    :type text: str
    """

    citation_sentences = {}
    sentences = tokeniser.tokenize(text)
    for sentence in sentences:
        print('sentence: {}'.format(sentence))
        for fmt, regex in REGEX_LIST_PDF.items():
            print('Trying regex: {}'.format(fmt))
            search = [i for i in regex.findall(sentence) if i !='']
            if search:
                for s in search:
                    citation_sentences[s] = sentence
                print('Found match: {}'.format(fmt))
                print(search)
                break
    return citation_sentences
