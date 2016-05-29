"""
Models use to define the database

The database is not initiated here, but a pointer is created named db. This is
to be passed to the app creator within the Flask blueprint.
"""

from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Article(db.Model):
    """
    Article table
    Signifies a single paper, that then links to the citations it makes
    to other known papers
    """
    __bind_key__ = 'article'
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    bibcode = db.Column(db.String)
    cites = db.relationship('Citations', backref='article')
    referenced_by = db.relationship('Citations', backref='article')

    def __repr__(self):
        return '<Article id:{0}, bibcode:{1}, citations:{2}>'\
            .format(self.id, self.bibcode, self.citations)


class Citations(db.Model):
    """
    Citation table
    Collection of the citations and sentiments of those citations
    from an article.
    """
    __bind_key__ = 'citations'
    __tablename__ = 'citations'
    id = db.Column(db.Integer, primary_key=True)
    citing_article = db.Column(db.Integer, db.ForeignKey('article.id'))
    references_article = db.Column(db.Integer, db.ForeignKey('article.id'))
    sentiment = db.Column(db.Float)

    def __repr__(self):
        return '<Citations, id: {0} cites_article: {1}, ' \
               'references_article {2}, sentiment: {3}' \
            .format(self.id, self.citing_article, self.references_article, self.sentiment)
