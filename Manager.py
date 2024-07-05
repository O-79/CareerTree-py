from GPT import GPT
import re

class College_Info:
    def __init__(self):
        self.LOC = None
        self.CAR = None
        self.JOB = None
        self.COL = None
        self.DEG = None
        self.TUT = None
        self.LON = None
        self.MTH_PAY = None
        self.LON_OPP = None

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

    def GET_MTH_PAY(self):
        return int(self.LON / self.MTH_PAY)
    
    def SET_MTH_PAY(self, MTH_PAY):
        self.MTH_PAY = MTH_PAY

    def GET_LON_OPP(self):
        return self.LON_OPP

    def SET_LON_OPP(self, LON_OPP):
        self.LON_OPP = LON_OPP

class Manager:
    def __init__(self):
        self.LOC = None
        self.CAR = None
        self.JOB = None
        self.COL = None
        self.DEG = None
        self.PAY = None
        self.INS = 1
        self.X = 0

    def INIT(self, X, INS):
        self.LOC = None
        self.CAR = None
        self.JOB = None
        self.COL = None
        self.DEG = None
        self.PAY = None
        self.INS = INS
        self.X = X

    def GET_LOC(self):
        return self.LOC

    def SET_LOC(self, LOC):
        self.LOC = LOC

    def GET_CAR_GPT(self):
        self.CAR = GPT.GET_ANS_TEST(f"NO EXTRA DESCRIPTION: list {self.X} careers in {self.LOC} AS A '|' SEPARATED LIST")
        return self.CAR

    def GET_CAR(self):
        return self.CAR

    def SET_CAR(self, CAR):
        self.CAR = CAR

    def GET_JOB_GPT(self):
        self.JOB = GPT.GET_ANS_TEST(f"NO EXTRA DESCRIPTION: list {self.X} jobs for {self.CAR} AS A '|' SEPARATED LIST")
        return self.JOB

    def GET_JOB(self):
        return self.JOB

    def SET_JOB(self, JOB):
        self.JOB = JOB

    def GET_COL_GPT(self):
        ADD = ""
        if self.INS == 1:
            ADD = " within " + self.LOC
        self.COL = GPT.GET_ANS_TEST(f"NO EXTRA DESCRIPTION: list {self.X} colleges (only their acronym) for a {self.JOB} job{ADD} AS A '|' SEPARATED LIST, NO REPEATS")
        return self.COL

    def GET_COL(self):
        return self.COL

    def SET_COL(self, COL):
        self.COL = COL

    def GET_PAY_GPT(self):
        self.PAY = int(float(GPT.GET_ANS_TEST_PAY(f"NO EXTRA DESCRIPTION, JUST ONE INTEGER: return the average annual pay for a {self.JOB} job in {self.LOC} in USD").replace('$', '').replace(',', '').replace('USD', '').strip()))
        return self.PAY

    def GET_DEG_GPT(self):
        self.DEG = GPT.GET_ANS_TEST_DEG(f"just state the name of the degree needed to get a job as a {self.JOB}, nothing else")
        if "Associate" in self.DEG:
            self.DEG = "Associate's degree"
        if "Bachelor" in self.DEG:
            self.DEG = "Bachelor's degree"
        if "Master" in self.DEG:
            self.DEG = "Master's degree"
        if "High" in self.DEG or "high" in self.DEG:
            self.DEG = "High school diploma"
        return self.DEG

    def GET_COL_INF_GPT(self):
        INF = College_Info()
        
        INF.SET_LOC(self.LOC)
        INF.SET_CAR(self.CAR)
        INF.SET_JOB(self.JOB)
        INF.SET_COL(self.COL)
        INF.SET_DEG(self.DEG)

        INS = GPT.GET_ANS_TEST_X(f"ANSWER WITH ONLY 1 LETTER (Y/N): is {self.COL} within the same state as {self.LOC}").lower() == 'y'

        if INS:
            TUT = int(float(GPT.GET_ANS_TEST_PAY(f"NO EXTRA DESCRIPTION, JUST ONE INTEGER: state the in-state tuition only at {self.COL} for a {self.DEG} degree in USD").replace('$', '').replace(',', '').replace('USD', '').strip()))
        else:
            TUT = int(float(GPT.GET_ANS_TEST_PAY(f"NO EXTRA DESCRIPTION, JUST ONE INTEGER: state the out-of-state tuition only at {self.COL} for a {self.DEG} degree in USD").replace('$', '').replace(',', '').replace('USD', '').strip()))
        INF.SET_TUT(TUT)

        LON = int(float(GPT.GET_ANS_TEST_PAY(f"NO EXTRA DESCRIPTION, JUST ONE INTEGER: state the average student loan taken at {self.COL} in USD").replace('$', '').replace(',', '').replace('USD', '').strip()))
        INF.SET_LON(LON)

        MTH_PAY = int(float(GPT.GET_ANS_TEST_PAY(f"NO EXTRA DESCRIPTION, JUST ONE INTEGER: state the monthly payment for a ${LON} loan in USD").replace('$', '').replace(',', '').replace('USD', '').strip()))
        INF.SET_MTH_PAY(MTH_PAY)

        LON_OPP = GPT.GET_ANS_TEST(f"NO EXTRA DESCRIPTION: list {self.X} loan repayment options AS A '|' SEPARATED LIST")
        LON_OPP = re.sub(r'[0-9]+', '', LON_OPP).replace(' .', '.').replace('. ', '.').replace('.', '').replace(' |', '|').replace('| ', '|').replace('\n', '|').replace('||', '|')
        INF.SET_LON_OPP(LON_OPP)

        return INF