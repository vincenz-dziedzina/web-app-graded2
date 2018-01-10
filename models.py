from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from settings import db

class Region(db.Model):
    __tablename__ = "region"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    state_id = db.Column(db.Integer, db.ForeignKey("region.id"))
    # backref creates a new property state which you can call
    constituencies = relationship("Region", backref=db.backref('state', remote_side=[id]))

    voteResults = relationship("VoteResult", back_populates="region")

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    voteResults = relationship("VoteResult", back_populates="category")

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class VoteResult(db.Model):
    __tablename__ = "voteResult"
    id = db.Column(db.Integer, primary_key=True)

    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
    region = relationship("Region", back_populates="voteResults")

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = relationship("Category", back_populates="voteResults")

    vote_type = db.Column(db.String(50), nullable=False)
    tentativeVotes = db.Column(db.Integer, default=0)
    priorPeriodVotes = db.Column(db.Integer, default=0)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

def test():
    category = Category(name="CDU")
    teltow = Region(name="teltow")
    brandenburg = Region(name="brandenburg")
    hennigsdorf = Region(name="hennigsdorf")
    voteResult = VoteResult(region=brandenburg, category=category, vote_type="Erststimmen", tentativeVotes=15, priorPeriodVotes=10)

    db.session.add(category)
    db.session.add(teltow)
    db.session.add(brandenburg)
    db.session.add(hennigsdorf)
    db.session.add(voteResult)
    db.session.commit()

    brandenburg.constuencies.append(teltow)
    brandenburg.constuencies.append(hennigsdorf)
    db.session.commit()

    teltow = Region.query.filter(Region.name == "teltow").first()
    brandenburg = Region.query.filter(Region.name == "brandenburg").first()
    hennigsdorf = Region.query.filter(Region.name == "hennigsdorf").first()

    print(brandenburg.constituencies)
    print(teltow.state.name)
    print(brandenburg.voteResults[0].tentativeVotes)
    print(party.voteResults[0].tentativeVotes)
    # print(hennigsdorf.state.name)

    # print(teltow.name)
    # print(teltow.state.name == brandenburg.name)
    # print(brandenburg.name)
    # print(brandenburg.state == None)
    # print(hennigsdorf.state.name == brandenburg.name)
#
#db.drop_all()
#db.create_all()
# test()
