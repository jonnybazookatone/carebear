"""
Test core utilities
"""

import app

from flask import current_app
from flask.ext.testing import TestCase

from carebear import get_sentences_latex, get_bbl_map
from models import db, Article, Citations

import unittest
import testing.postgresql


class TestCaseDatabase(TestCase):
    """
    Base test class for when databases are being used.
    """

    postgresql_url_dict = {
        'port': 1234,
        'host': '127.0.0.1',
        'user': 'postgres',
        'database': 'test'
    }
    postgresql_url = 'postgresql://{user}@{host}:{port}/{database}'\
        .format(
            user=postgresql_url_dict['user'],
            host=postgresql_url_dict['host'],
            port=postgresql_url_dict['port'],
            database=postgresql_url_dict['database']
        )

    def create_app(self):
        """
        Create the wsgi application

        :return: application instance
        """
        app_ = app.create_app()
        app_.config['SQLALCHEMY_DATABASE_URI'] = \
            TestCaseDatabase.postgresql_url
        return app_

    @classmethod
    def setUpClass(cls):
        cls.postgresql = \
            testing.postgresql.Postgresql(**cls.postgresql_url_dict)

    @classmethod
    def tearDownClass(cls):
        cls.postgresql.stop()

    def setUp(self):
        """
        Set up the database for use
        """

        current_app.logger.info('Setting up db on: {0}'
                                .format(current_app.config['SQLALCHEMY_BINDS']))
        db.create_all()

    def tearDown(self):
        """
        Remove/delete the database and the relevant connections

        :return: no return
        """
        db.session.remove()
        db.drop_all()

    def test_can_add_article_model(self):
        """
        Test can extract and store the sentiment of records
        """

        a1 = Article(bibcode='bib1')
        a2 = Article(bibcode='bib2')
        db.session.add_all([a1, a2])
        db.session.commit()

        # So let's say bib1 (citing_article) gives a nice reference to the
        # article bib2 (references_article)
        c1 = Citations(
            sentiment=1.0,
            citing_article=a1,
            references_article=a2
        )

        db.session.add_all([a1, a2, c1])
        db.session.commit()

        self.assertEqual(
            Article.query.filter(Article.bibcode == 'bib1').one(),
            a1
        )

        self.assertEqual(
            len(Citations.query.filter(Citations.citing_article_id == a1.id).all()),
            1
        )


class TestRegex(unittest.TestCase):
    """
    Test regex on some things we expect to be able to find from the fulltext.
    """
    def test_get_citep(self):
        """
        Get all citations with citep
        """
        text = (
            'This is useless text, some normal science. '
            'This is some relevant citation \citep{Author96} and another one'
            'here \citep{SecondAuthor98}. But '
            'this also has no citation.'
        )
        sentences = get_sentences_latex(text)

        extracted = list(sentences.keys())
        expected = ['Author96', 'SecondAuthor98']
        self.assertListEqual(
            extracted,
            expected
        )

    def test_get_citet(self):
        """
        Get all citations with citep
        """
        text = (
            'This is useless text, some normal science. '
            'This is some relevant citation \citet{Author96} and another one'
            'here \citet{SecondAuthor98}. But '
            'this also has no citation.'
        )
        sentences = get_sentences_latex(text)

        extracted = list(sentences.keys())
        expected = ['Author96', 'SecondAuthor98']
        self.assertListEqual(
            extracted,
            expected
        )

    def test_get_citealt(self):
        """
        Get all citations with citep
        """
        text = (
            'This is useless text, some normal science. '
            'This is some relevant citation \citealt{Author96} and another one'
            'here \citealt{SecondAuthor98}. But '
            'this also has no citation.'
        )
        sentences = get_sentences_latex(text)

        extracted = list(sentences.keys())
        expected = ['Author96', 'SecondAuthor98']
        self.assertListEqual(
            extracted,
            expected
        )

    def test_load_bbl(self):
        """
        Test we can load BBL file and create a hashmap for entries
        """
        text = (
            '\\bibitem[{{Ahn} {et~al}\mbox{.}(2012){Ahn}, {Alexandroff}, {Allende Prieto},'
            '{Anderson}, {Anderton}, {Andrews}, {Aubourg}, {Bailey}, {Balbinot}, {Barnes},'
            '\& et~al.}]{sdssdr9}'
            '{Ahn} C.~P. {et~al.}, 2012, ApJS, 203, 21'
            ''
            '\\bibitem[{{Amorisco}(2014)}]{amorisco_2014}'
            '{Amorisco} N.~C., 2014, ArXiv e-prints'
        )

        bbl_map = get_bbl_map(text)
        expected_map = ['sdssdr9', 'amorisco_2014']
        self.assertListEqual(
            list(bbl_map.keys()),
            expected_map

        )

    # def test_in_bracket_et_al(self):
    #     """
    #     Test when it is in brackets with et al, form: (Author et al. YYYY)
    #     """
    #     text = (
    #         'This is useless text, some normal science. '
    #         'This is some relevant citation (Jdizzle et al. 2015). But '
    #         'this also has no citation.'
    #     )
    #     sentences = get_sentences(text)
    #
    #     self.assertEqual(
    #         len(sentences.keys()),
    #         1
    #     )
    #     self.assertIn('Jdizzle', sentences.keys()[0])
    #
    # def test_in_bracket_single(self):
    #     """
    #     Test when it is in brackets one author, form: (Author YYYY)
    #     """
    #     text = (
    #         'This is useless text, some normal science. '
    #         'This is some relevant citation (Jdizzle 2015). But '
    #         'this also has no citation.'
    #     )
    #     sentences = get_sentences(text)
    #
    #     self.assertEqual(
    #         len(sentences.keys()),
    #         1
    #     )
    #     self.assertIn('Jdizzle', sentences.keys()[0])
    #
    # def test_in_sentence_date_brackets(self):
    #     """
    #     Test when the year is in brackets, \citet{}: Author et al. (YYYY)
    #     """
    #     text = (
    #         'This is useless text, some normal science. '
    #         'This is some relevant citation Jdizzle et al. (2015). But '
    #         'this also has no citation.'
    #     )
    #     sentences = get_sentences(text)
    #
    #     self.assertEqual(
    #         len(sentences.keys()),
    #         1
    #     )
    #     self.assertIn('Jdizzle', sentences.keys()[0])
    #
    # def test_in_sentence_date_brackets_single(self):
    #     """
    #     Test when the year is in brackets one author, \citet{}: Author (YYYY)
    #     """
    #     text = (
    #         'This is useless text, some normal science. '
    #         'This is some relevant citation Jdizzle (2015). But '
    #         'this also has no citation.'
    #     )
    #     sentences = get_sentences(text)
    #
    #     self.assertEqual(
    #         len(sentences.keys()),
    #         1
    #     )
    #     self.assertIn('Jdizzle', sentences.keys()[0])
    #
    # def test_multiple_citations_in_one_sentence(self):
    #     """
    #     Test when there are multiple citations in one entry
    #     """
    #     text = (
    #         'This is a citation (Jdizzle et al. 2015) and also this '
    #         'is a citation (Jdazzle et al. 2015).'
    #     )
    #     sentences = get_sentences(text)
    #     self.assertEqual(
    #         len(sentences.keys()),
    #         2
    #     )
    #

    # Some notes
    #
    # If the article does not exist: add Article
    # For each citation: if it does not exist add Article
    #                  : also add a Citations object linking the two
    #
    # Do simple sentiment analysis:
    #   1. regex for (Author (et al.) YYYY) should be a nice start
    #   2. extract just the sentance, and then check the sentiment
    #      >0: positive
    #      <0: negative
