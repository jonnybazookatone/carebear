# Carebear O'Meter

![Picture of pink fluffly carebear](carebear.jpg)

Should we care about someones papers, or are they consistently hated on through their citations?

This is the first pipeline to look at sentiment within the articles of the ADS corpus.

# Specification

For each document, could do the following:

  1. Find all the references within the document
    * regex in the LaTeX or 'normal' content
  2. Convert the sentence into a sentiment score
