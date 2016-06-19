# encoding: utf8
"""
Helper functions to run different utilities
"""

import argparse
from carebear import (
    get_sentences_latex,
    get_bbl_map,
    get_sentinment
)


def main(latex_file, bbl_file):

    with open(latex_file, 'r') as f:
        latex = f.read()
    with open(bbl_file, 'r') as f:
        bbl = f.read()

    sentences = get_sentences_latex(latex)
    bbl_map = get_bbl_map(bbl)

    sentiment = {}
    for key, value in sentences.iteritems():

        sentiment[bbl_map[key]] = get_sentinment(value)

    for key, value in sentiment.iteritems():
        print('Cites {} and thinks it is: {}'.format(
            key,
            value
        ))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--latex', dest='latex', required=True, help='Path to .latex')
    parser.add_argument('--bbl', dest='bbl', required=True, help='Path to .bbl')
    args = parser.parse_args()

    main(latex_file=args.latex, bbl_file=args.bbl)
