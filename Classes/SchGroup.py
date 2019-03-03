class SchGroup:
    def __init__(self):
        self.lecture = None
        self.tutorials = []
        self.labs = []
        self.number = None
        self.courseTerm = ''

    def setLecture(self, lecture):
        self.lecture = lecture
        # self.daysTaken.add(lecture.time.day)

    def add_lab(self, lab):
        self.labs.append(lab)
        # self.daysTaken.add(lab.time.day)

    def add_tut(self, tut):
        self.tutorials.append(tut)
        # self.daysTaken.add(tut.time.day)