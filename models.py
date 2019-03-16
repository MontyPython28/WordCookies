from wordc import db

class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    letters = db.Column(db.String(20))
    count = db.Column(db.Integer)

    def __repr__(self):
        return '<Counter {}>'.format(self.letters) 

