from models import db, VotingStatus

def is_voting_active():
    status = db.session.execute(
        db.select(VotingStatus)
    ).scalar()
    return status.is_active


def start_voting():
    status = db.session.execute(db.select(VotingStatus)).scalar()
    if status.is_active == False:
        status.is_active = True
        db.session.commit()


def stop_voting():
    status = db.session.execute(db.select(VotingStatus)).scalar()
    if status.is_active == True:
        status.is_active = False
        db.session.commit()


