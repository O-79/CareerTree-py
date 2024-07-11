class CTree_Node:
    def __init__(self):
        self.ARR = []
        self.DAT = None

    def GET_ARR(self):
        return self.ARR

    def GET(self):
        return self.DAT

    def SET(self, DAT):
        self.DAT = DAT

class CTree:
    def __init__(self):
        self.ROT = CTree_Node()
        self.ROT.SET(None)
        self.DEP = 0

    def SER_CAR(self, CAR):
        NOD_1 = self.ROT
        _FND_ = False
        for node in NOD_1.GET_ARR():
            if node.GET() == CAR:
                _FND_ = True

        if not _FND_:
            NOD_X = CTree_Node()
            NOD_X.SET(CAR)
            NOD_1.GET_ARR().append(NOD_X)
            if self.DEP == 0:
                self.DEP = 1
        return not _FND_

    def SER_JOB(self, CAR, JOB):
        NOD_1 = self.ROT
        NOD_2 = CTree_Node()
        for node in NOD_1.GET_ARR():
            if node.GET() == CAR:
                NOD_2 = node

        _FND_ = False
        for node in NOD_2.GET_ARR():
            if node.GET() == JOB:
                _FND_ = True

        if not _FND_:
            NOD_X = CTree_Node()
            NOD_X.SET(JOB)
            NOD_2.GET_ARR().append(NOD_X)
            if self.DEP == 1:
                self.DEP = 2
        return not _FND_

    def SER_COL(self, CAR, JOB, COL):
        NOD_1 = self.ROT
        NOD_2 = CTree_Node()
        for node in NOD_1.GET_ARR():
            if node.GET() == CAR:
                NOD_2 = node

        NOD_3 = CTree_Node()
        for node in NOD_2.GET_ARR():
            if node.GET() == JOB:
                NOD_3 = node

        _FND_ = False
        for node in NOD_3.GET_ARR():
            if node.GET() == COL:
                _FND_ = True

        if not _FND_:
            NOD_X = CTree_Node()
            NOD_X.SET(COL)
            NOD_3.GET_ARR().append(NOD_X)
            if self.DEP == 2:
                self.DEP = 3
        return not _FND_

    def ADD(self, LVL, LOC, CAR, JOB, COL):
        if LVL == 0:
            self.ROT = CTree_Node()
            self.ROT.SET(LOC)
            self.DEP = 0
            return True
        elif LVL == 1:
            return self.SER_CAR(CAR)
        elif LVL == 2:
            return self.SER_JOB(CAR, JOB)
        elif LVL == 3:
            return self.SER_COL(CAR, JOB, COL)
        return False

    def STR(self):
        s = []
        s.append(f"LOC {self.ROT.GET()}")
        for A in self.ROT.GET_ARR():
            if A == self.ROT.GET_ARR()[-1]:
                s.append(f" └── CAR {A.GET()}")
            else:
                s.append(f" ├── CAR {A.GET()}")
            for B in A.GET_ARR():
                if B == A.GET_ARR()[-1]:
                    s.append(f"      └── JOB {B.GET()}")
                else:
                    s.append(f"      ├── JOB {B.GET()}")
                for C in B.GET_ARR():
                    if C == B.GET_ARR()[-1]:
                        s.append(f"           └── COL {C.GET()}")
                    else:
                        s.append(f"           ├── COL {C.GET()}")
        return "\n".join(s)