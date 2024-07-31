from GPT import GPT
import re

class College_Info:
    def __init__(self):
        self.INF = {
            'LOC': None,
            'CAR': None,
            'JOB': None,
            'PAY_LOW': None,
            'PAY_UPP': None,
            'COL': None,
            'DEG': None,
            'REQ': None,
            'TUT': None,
            'LON': None,
            'MTH_PAY': None,
            'LON_OPP': None
        }

    def GET(self, KEY: str):
        return self.INF.get(KEY)

    def SET(self, KEY: str, VAL: str):
        self.INF[KEY] = VAL

    def GET_MTH_PAY(self):
        if self.INF['LON'] and self.INF['MTH_PAY']:
            return int(self.INF['LON'] / self.INF['MTH_PAY'])
        return 'N/A'

class Manager:
    def __init__(self, X: int, INS: int):
        self.X = X
        self.INS = INS
        self.CUR = {
            'LOC': None,
            'CAR': None,
            'JOB': None,
            'COL': None,
            'DEG': None,
            'PAY_LOW': None,
            'PAY_UPP': None,
            'PAY': None
        }

    def SET_X(self, X: int):
        self.X = X

    def SET_INS(self, INS: int):
        self.INS = INS

    def GET(self, KEY: str):
        return self.CUR.get(KEY)

    def SET(self, KEY: str, VAL: str):
        self.CUR[KEY] = VAL

    def GET_CAR_GPT(self):
        self.CUR['CAR'] = GPT.GET_ANS(f"NO EXTRA DESCRIPTION: list {self.X} careers in {self.CUR['LOC']} AS A '|' SEPARATED LIST")
        return self.CUR['CAR']

    def GET_JOB_GPT(self):
        self.CUR['JOB'] = GPT.GET_ANS(f"NO EXTRA DESCRIPTION: list {self.X} jobs for {self.CUR['CAR']} AS A '|' SEPARATED LIST")
        return self.CUR['JOB']

    def GET_COL_GPT(self):
        ADD = ""
        if self.INS == 1:
            ADD = " within or close to " + self.CUR['LOC']
        self.CUR['COL'] = GPT.GET_ANS(f"NO EXTRA DESCRIPTION: list {self.X} colleges (no acronyms) for a {self.CUR['JOB']} job{ADD} AS A '|' SEPARATED LIST, NO REPEATS")
        return self.CUR['COL']

    def GET_PAY_GPT(self):
        self.CUR['PAY_LOW'] = self.INT(GPT.GET_ANS(f"NO EXTRA DESCRIPTION, JUST ONE INTEGER: return the average annual pay for a entry-level {self.CUR['JOB']} job in {self.CUR['LOC']} in USD"))
        self.CUR['PAY_UPP'] = self.INT(GPT.GET_ANS(f"NO EXTRA DESCRIPTION, JUST ONE INTEGER: return the average annual pay for a senior-level {self.CUR['JOB']} job in {self.CUR['LOC']} in USD"))
        self.CUR['PAY'] = "Entry: " + str(self.CUR['PAY_LOW']) + " | Senior: " + str(self.CUR['PAY_UPP'])
        return self.CUR['PAY']

    def GET_DEG_GPT(self):
        self.CUR['DEG'] = GPT.GET_ANS(f"just state the full name of the specific degree needed to get a job as a {self.CUR['JOB']}, nothing else")
        return self.CUR['DEG']

    def GET_COL_DSC_GPT(self):
        return GPT.GET_ANS(f"tell me more about {self.CUR['COL']}")
    
    def GET_DBG_GPT(self, Q: str):
        return GPT.GET_ANS(Q);
    
    def GET_EXT_GPT(self, Q: str):
        return GPT.GET_ANS_TEMP_TOPP("only answer the following question if it relates to career path guidance, types of careers or information about specific careers, types of jobs or information about specific jobs, types of colleges / universities or information about specific colleges / universities, or other on-topic subjects, ELSE RESPOND WITH 'Please ask a related question.'; QUESTION: " + Q, 0.7, 0.7)

    def GET_SUM_GPT(self, CAREER_TREE):
        return GPT.GET_ANS_TEMP_TOPP_SYS(f"give a detailed summary and career recommendations from the following career tree: \n```{CAREER_TREE.STR().replace("CAR", "Career: ").replace("JOB", "Job: ").replace("COL", "College: ")}```", 0.7, 0.7, "USE MARKDOWN (.MD) FORMATTING, FEEL FREE TO USE HEADERS, BOLDING, ITALICS, LISTS, ETC. AS NEEDED")

    def GET_COL_INF_GPT(self):
        INF = College_Info()
        
        INF.SET('CAR', self.CUR['CAR'])
        INF.SET('JOB', self.CUR['JOB'])
        INF.SET('COL', self.CUR['COL'])
        INF.SET('DEG', self.CUR['DEG'])
        INF.SET('PAY_LOW', self.CUR['PAY_LOW'])
        INF.SET('PAY_UPP', self.CUR['PAY_UPP'])       
        
        INF.SET('LOC', GPT.GET_ANS(f"where is {self.CUR['COL']}? RESPOND IN THE FORMAT (State is optional): City, State, Country"))
        
        REQ = GPT.GET_ANS(f"NO EXTRA DESCRIPTION: state the required unweighted GPA (must be between 0.0 - 4.0), SAT, and ACT scores needed for {self.CUR['COL']} IN THE FORMAT: 'GPA: #, SAT: #, ACT: #'")
        INF.SET('REQ', REQ)

        INS = GPT.GET_ANS(f"ANSWER WITH ONLY 1 LETTER (Y/N): is {self.CUR['COL']} within the same state as {self.CUR['LOC']}").lower() == 'y'

        if INS:
            TUT = self.INT(GPT.GET_ANS(f"NO EXTRA DESCRIPTION, JUST ONE INTEGER: state the in-state tuition only at {self.CUR['COL']} for a {self.CUR['DEG']} degree in USD"))
        else:
            TUT = self.INT(GPT.GET_ANS(f"NO EXTRA DESCRIPTION, JUST ONE INTEGER: state the out-of-state tuition only at {self.CUR['COL']} for a {self.CUR['DEG']} degree in USD"))
        INF.SET('TUT', TUT)

        LON = self.INT(GPT.GET_ANS(f"NO EXTRA DESCRIPTION, JUST ONE INTEGER: state the average student loan taken at {self.CUR['COL']} in USD"))
        INF.SET('LON', LON)

        MTH_PAY = self.INT(GPT.GET_ANS(f"NO EXTRA DESCRIPTION, JUST ONE INTEGER: state the monthly payment for a ${LON} loan in USD"))
        INF.SET('MTH_PAY', MTH_PAY)

        LON_OPP = "[WIP]" # GPT.GET_ANS(f"NO EXTRA DESCRIPTION: list {self.X} loan repayment options AS A '|' SEPARATED LIST")
        # LON_OPP = re.sub(r'[0-9]+', '', LON_OPP).replace(' .', '.').replace('. ', '.').replace('.', '').replace(' |', '|').replace('| ', '|').replace('\n', '|').replace('||', '|')
        INF.SET('LON_OPP', LON_OPP)
        
        return INF

    def INT(self, XYZ: str):
        return int(float(XYZ.replace('$', '').replace(',', '').replace('USD', '').strip()))