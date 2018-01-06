import csv
import sys
from models import Region, Category, VoteResult
from settings import db
from flask_sqlalchemy import SQLAlchemy

if(len(sys.argv) < 1):
    sys.exit("no path given")

db.drop_all()
db.create_all()

def writeCategoriesToDB(row):
    tempParties = []

    for i in range(3, len(row)-1, 4):
        category_name = row[i]
        if category_name:
            db.session.add(Category(name=category_name))

    db.session.commit()

def isState(row):
    return row[2] == "99" or row[1] == "Bundesgebiet"

def writeRowToDB(row, constituencies):
    if not emptyLine(row):
        region_name = row[1]
        region = None

        if isState(row):
            #state
            region = Region(name=region_name)
            db.session.add(region)

            for constituency in constituencies:
                region.constituencies.append(constituency)
                db.session.add(constituency)
            constituencies = []
        else:
            #constuency
            region = Region(name=region_name)
            constituencies.append(region)

        writeVoteResultsToDB(row, region)
        db.session.commit()

    return constituencies

def writeVoteResultsToDB(row, region):
    category_index = 1
    for i in range(3, len(row)-1, 4):
        category = Category.query.get(category_index)

        tentativeVotes = row[i] if row[i] else 0
        priorPeriodVotes = row[i+1] if row[i+1] else 0
        voteResult1 = VoteResult(region=region, category=category, tentativeVotes=tentativeVotes, priorPeriodVotes=priorPeriodVotes, vote_type="Erststimmen")
        db.session.add(voteResult1)

        tentativeVotes = row[i+2] if row[i+2] else 0
        priorPeriodVotes = row[i+3] if row[i+3] else 0
        voteResult2 = VoteResult(region=region, category=category, tentativeVotes=tentativeVotes, priorPeriodVotes=priorPeriodVotes, vote_type="Zweitstimmen")
        db.session.add(voteResult2)
        category_index += 1

def emptyLine(row):
    return len(row) < 3

path = sys.argv[1]
with open(path) as csvfile:
    reader = csv.reader(csvfile, delimiter=";")
    constituencies = []
    try:
        for index, row in enumerate(reader):
            if(index + 1 == 3):
                writeCategoriesToDB(row)
            if(index + 1 > 5):
                constituencies = writeRowToDB(row, constituencies)
    except csv.Error as e:
        sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
