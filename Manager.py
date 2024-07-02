from re import S
from GPT import GPT

class College_Info:

    def __init__(self):
        self.LOC = None
        self.CAR = None
        self.JOB = None
        self.COL = None
        self.DEG = None
        self.TUT = 0
        self.LON = 0
        self.LON_OPP = []
        self.MTH_PAY = 0.0

    def GET_LOC(self):
        return self.LOC

    def SET_LOC(self, LOC):
        self.LOC = LOC

    def GET_CAR(self):
        return self.CAR

    def SET_CAR(self, CAR):
        self.CAR = CAR

    def GET_JOB(self):
        return self.JOB

    def SET_JOB(self, JOB):
        self.JOB = JOB

    def GET_COL(self):
        return self.COL

    def SET_COL(self, COL):
        self.COL = COL

    def GET_DEG(self):
        return self.DEG

    def SET_DEG(self, DEG):
        self.DEG = DEG

    def GET_TUT(self):
        return self.TUT

    def SET_TUT(self, TUT):
        self.TUT = TUT

    def GET_LON(self):
        return self.LON

    def SET_LON(self, LON):
        self.LON = LON

    def GET_LON_OPP(self):
        return self.GET_LON_OPP

    def SET_LON_OPP(self, LON_OPP):
        self.LON_OPP = LON_OPP    

    def GET_MTH_PAY(self):
        return self.MTH_PAY

class Manager:

    def __init__(self):
        self.LOC = None
        self.CAR = None
        self.JOB = None
        self.COL = None
        self.DEG = None
        self.PAY = None
        self.X = 0

    def INIT(self, X):
        self.LOC = None
        self.CAR = None
        self.JOB = None
        self.COL = None
        self.DEG = None
        self.PAY = None
        self.X = X

    def GET_LOC(self):
        return self.LOC

    def SET_LOC(self, LOC):
        self.LOC = LOC

    def GET_CAR_GPT(self):
        self.CAR = GPT.GET_ANS_TEST(f"NO EXTRA DESCRIPTION: list the top {self.X} careers in {self.LOC} AS A COMMA-DELIMITED LIST WITHOUT NUMBERING")
        return self.CAR

    def GET_CAR(self):
        return self.CAR

    def SET_CAR(self, CAR):
        self.CAR = CAR

    def GET_JOB_GPT(self):
        self.JOB = GPT.GET_ANS_TEST(f"NO EXTRA DESCRIPTION: list the top {self.X} jobs for {self.CAR} AS A COMMA-DELIMITED LIST WITHOUT NUMBERING")
        return self.JOB

    def GET_JOB(self):
        return self.JOB

    def SET_JOB(self, JOB):
        self.JOB = JOB

    def GET_COL_GPT(self):
        self.COL = GPT.GET_ANS_TEST(f"NO EXTRA DESCRIPTION: list the top {self.X} colleges for a {self.JOB} job AS A COMMA-DELIMITED LIST WITHOUT NUMBERING")
        return self.COL

    def GET_COL(self):
        return self.COL

    def SET_COL(self, COL):
        self.COL = COL

    def GET_PAY_GPT(self):
        self.PAY = GPT.GET_ANS_TEST_PAY(f"NO EXTRA DESCRIPTION, SIMPLE INTEGER WITH NO FORMATTING: return the average annual pay for a {self.JOB} job in {self.LOC}")
        return self.PAY

    def GET_DEG_GPT(self):
        self.DEG = GPT.GET_ANS_TEST_DEG(f"NO EXTRA DESCRIPTION: state the degree needed to get a job as a {self.JOB}")
        return self.DEG

    def GET_COL_INF_GPT(self):
        INF = College_Info()

        INF.LOC = self.LOC
        INF.CAR = self.CAR
        INF.JOB = self.JOB
        INF.COL = self.COL
        INF.DEG = self.DEG

        INS = GPT.GET_ANS_TEST_X(f"ANSWER WITH ONLY 1 LETTER (Y/N): is {self.LOC} in the same state as {self.COL}").lower() == 'y'

        if INS:
            TUT = int(GPT.GET_ANS_TEST_PAY(f"NO EXTRA DESCRIPTION, SIMPLE INTEGER WITH NO FORMATTING: state the in-state tuition at {self.COL} for a {self.DEG} degree"))
        else:
            TUT = int(GPT.GET_ANS_TEST_PAY(f"NO EXTRA DESCRIPTION, SIMPLE INTEGER WITH NO FORMATTING: state the out-of-state tuition at {self.COL} for a {self.DEG} degree"))
        INF.TUT = TUT

        LON = int(GPT.GET_ANS_TEST_PAY(f"NO EXTRA DESCRIPTION, SIMPLE INTEGER WITH NO FORMATTING: state the average loan taken at {self.COL}"))
        INF.LON = LON

        LON_OPP = GPT.GET_ANS_TEST(f"NO EXTRA DESCRIPTION: list the top {self.X} loan repayment options AS A COMMA-DELIMITED LIST WITHOUT NUMBERING")
        INF.LON_OPP = LON_OPP.split(",")

        MTH_PAY = float(GPT.GET_ANS_TEST_PAY(f"NO EXTRA DESCRIPTION, SIMPLE NUMBER ONLY: state the monthly payment for a ${LON} loan"))
        INF.MTH_PAY = MTH_PAY

        return INF