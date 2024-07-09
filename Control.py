from typing import List
from CTree import CTree
from Manager import Manager
import re
from datetime import datetime
import os

class Control:
    MENU = "\nWELCOME-TO-THE-CAREER-TREE------\n" \
           + "USING:-gpt-turbo-3.5------------\n" \
           + "--CMD-MENU----------------------\n" \
           + "----\"(L)OC\"-:--LOC-CAR-JOB-COL--\n" \
           + "--------RESETS-TREE-------------\n" \
           + "----\"(C)AR\"-:--CAR-JOB-COL------\n" \
           + "----\"(J)OB\"-:--JOB-COL----------\n" \
           + "----\"(U)COL\":--COL--------------\n" \
           + "----\"(Q)UIT\":--QUIT-------------\n\n"

    Q_SIZ = "* Size of responses ? (4 [Faster] - 16 [Slower])"
    
    Q_INS = "* In-state colleges only? (0 [No] / 1 [Yes])"

    Q_LOC = "* Enter your current / desired location"

    Q_CAR = "* Choose one of the following careers (add / select)"

    Q_JOB = "* Choose one of the following jobs (add / select)"

    Q_COL = "* Choose one of the following colleges (add / select)"

    A_DEG = "* You will need the following degree: "

    A_PAY = "* Salary: "

    @staticmethod
    def PARSE(Q: str, TYP: str, X: int, MGR):
        print(Q)
        XYZ = ""
        if TYP == "CAR":
            XYZ = MGR.GET_CAR_GPT()
        elif TYP == "JOB":
            XYZ = MGR.GET_JOB_GPT()
        elif TYP == "COL":
            XYZ = MGR.GET_COL_GPT()
        
        XYZ = re.sub(r'[0-9]+', '', XYZ).replace(' .', '.').replace('. ', '.').replace('.', '').replace(' |', '|').replace('| ', '|').replace('\n', '|').replace('||', '|')
        
        X = XYZ.count('|') + 1

        print(f"* Choose (1 - {X}):\n{XYZ}")
        try:
            SEL = int(input())
        except ValueError:
            SEL = 1

        if SEL < 1:
            SEL = 1
        if SEL > X:
            SEL = X
        
        XYZ_SEL = XYZ.split('|')[SEL - 1].strip()

        if TYP == "CAR":
            MGR.SET_CAR(XYZ_SEL)
        elif TYP == "JOB":
            MGR.SET_JOB(XYZ_SEL)
        elif TYP == "COL":
            MGR.SET_COL(XYZ_SEL)

        if TYP == "JOB":
            print(f"{Control.A_DEG}{MGR.GET_DEG_GPT()}\n{Control.A_PAY}{MGR.GET_PAY_GPT()}")

        return XYZ_SEL

    @staticmethod
    def CMD_LOC(CAREER_TREE, X: int, MGR):
        print(Control.Q_LOC, end='')
        if MGR.GET_LOC() is not None:
            print(" (resets tree)")
        else:
            print()

        LOC_INP = input()
        LOC_ADD = LOC_INP[0].upper() + LOC_INP[1:]
        MGR.SET_LOC(LOC_ADD)

        CAR_ADD = Control.PARSE(Control.Q_CAR, "CAR", X, MGR)
        JOB_ADD = Control.PARSE(Control.Q_JOB, "JOB", X, MGR)
        COL_ADD = Control.PARSE(Control.Q_COL, "COL", X, MGR)

        CAREER_TREE.ADD(0, LOC_ADD, CAR_ADD, JOB_ADD, COL_ADD)
        CAREER_TREE.ADD(1, LOC_ADD, CAR_ADD, JOB_ADD, COL_ADD)
        CAREER_TREE.ADD(2, LOC_ADD, CAR_ADD, JOB_ADD, COL_ADD)

        return MGR.GET_COL_INF_GPT() if CAREER_TREE.ADD(3, LOC_ADD, CAR_ADD, JOB_ADD, COL_ADD) else None

    @staticmethod
    def CMD_CAR(CAREER_TREE, X: int, MGR):
        CAR_ADD = Control.PARSE(Control.Q_CAR, "CAR", X, MGR)
        JOB_ADD = Control.PARSE(Control.Q_JOB, "JOB", X, MGR)
        COL_ADD = Control.PARSE(Control.Q_COL, "COL", X, MGR)

        CAREER_TREE.ADD(1, MGR.GET_LOC(), CAR_ADD, JOB_ADD, COL_ADD)
        CAREER_TREE.ADD(2, MGR.GET_LOC(), CAR_ADD, JOB_ADD, COL_ADD)

        return MGR.GET_COL_INF_GPT() if CAREER_TREE.ADD(3, MGR.GET_LOC(), CAR_ADD, JOB_ADD, COL_ADD) else None

    @staticmethod
    def CMD_JOB(CAREER_TREE, X: int, MGR):
        JOB_ADD = Control.PARSE(Control.Q_JOB, "JOB", X, MGR)
        COL_ADD = Control.PARSE(Control.Q_COL, "COL", X, MGR)

        CAREER_TREE.ADD(2, MGR.GET_LOC(), MGR.GET_CAR(), JOB_ADD, COL_ADD)

        return MGR.GET_COL_INF_GPT() if CAREER_TREE.ADD(3, MGR.GET_LOC(), MGR.GET_CAR(), JOB_ADD, COL_ADD) else None

    @staticmethod
    def CMD_COL(CAREER_TREE, X: int, MGR):
        COL_ADD = Control.PARSE(Control.Q_COL, "COL", X, MGR)

        return MGR.GET_COL_INF_GPT() if CAREER_TREE.ADD(3, MGR.GET_LOC(), MGR.GET_CAR(), MGR.GET_JOB(), COL_ADD) else None

    @staticmethod
    def DSH(TXT: str) -> str:
        if len(TXT) > 32:
            return "--------------------------------"

        TXT.replace(' ', '-')
        X = 32 - len(TXT)

        LIN = '-' * (X // 2) + TXT + '-' * (X // 2)
        if X % 2 == 1:
            LIN += '-'

        return LIN

    @staticmethod
    def main():
        PATH = os.path.join(os.path.normpath(os.path.expanduser("~/Desktop")), "output")
        if not os.path.exists(PATH):
            os.makedirs(PATH)
        
        MGR = Manager()
        CAREER_TREE = CTree()
        COLLEGE_INFO: List[Manager.College_Info] = []

        X = 0
        print(Control.Q_SIZ)
        try:
            X = int(input())
            if X < 4:
                X = 4
            if X > 16:
                X = 16
        except ValueError:
            X = 10
        
        INS = -1 # 0: OOS , 1: INS
        print(Control.Q_INS)
        try:
            INS = int(input())
            if INS != 0 and INS != 1:
                INS = 1
        except ValueError:
            INS = 1
        
        MGR.INIT(X, INS)

        print(Control.MENU, end='')

        CMD = "loc"
        while CMD.lower() not in ["quit", "exit", "q"]:
            INF = None

            if CMD.lower() in ["loc", "location", "l"]:
                INF = Control.CMD_LOC(CAREER_TREE, X, MGR)

            if CMD.lower() in ["car", "career", "c"]:
                INF = Control.CMD_CAR(CAREER_TREE, X, MGR)

            if CMD.lower() in ["job", "position", "j"]:
                INF = Control.CMD_JOB(CAREER_TREE, X, MGR)

            if CMD.lower() in ["col", "college", "uni", "university", "u"]:
                INF = Control.CMD_COL(CAREER_TREE, X, MGR)

            if INF:
                COLLEGE_INFO.append(INF)

            print("\n>", end=" ")
            CMD = input()

        print(f"\n{Control.DSH('TREE')}\n{CAREER_TREE.LST()}\n{Control.DSH('')}")

        print(f"\n{Control.DSH('COLLEGE REPORT')}")
        if not COLLEGE_INFO:
            print("no colleges\n" + Control.DSH(''))
        for I in COLLEGE_INFO:
            print(f"NAME:       {I.GET_COL()}")
            print(f"LOCATION:   {I.GET_LOC()}")
            print(f"DEGREE:     {I.GET_DEG()}")
            print(f"REQS:       {I.GET_REQ()}")
            print(f"CAREER:     {I.GET_CAR()}")
            print(f"JOB:        {I.GET_JOB()}")
            print(f"TUITION:    {I.GET_TUT()}") # include total expenses
            print(f"LOAN:       {I.GET_LON()} (avg.)") # WIP
            print(f"REPAY IN:   {I.GET_MTH_PAY()} months (est.)") # WIP
            # print(f"PROGRAMS:   {I.GET_LON_OPP()}") # WIP
            print(Control.DSH(''))
        
        STR_TIME = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
        os.makedirs(os.path.join(PATH, STR_TIME))
        
        F_NAME_CTREE = "Tree_" + STR_TIME + ".txt"
        PATH_CTREE = os.path.join(os.path.join(PATH, STR_TIME), F_NAME_CTREE)
        with open(PATH_CTREE, 'w', encoding="utf-8") as F:
            F.write(f"{Control.DSH('TREE')}\n{CAREER_TREE.LST()}\n{Control.DSH('')}")
            F.close()
        
        if COLLEGE_INFO:
            F_NAME_COLREP = "Report_" + STR_TIME + ".txt"
            PATH_COLREP = os.path.join(os.path.join(PATH, STR_TIME), F_NAME_COLREP)
            with open(PATH_COLREP, 'w', encoding="utf-8") as F:
                F.write(f"{Control.DSH('COLLEGE REPORT')}\n")
                for I in COLLEGE_INFO:
                    F.write(f"NAME:       {I.GET_COL()}\n")
                    F.write(f"LOCATION:   {I.GET_LOC()}\n")
                    F.write(f"DEGREE:     {I.GET_DEG()}\n")
                    F.write(f"REQS:       {I.GET_REQ()}\n")
                    F.write(f"CAREER:     {I.GET_CAR()}\n")
                    F.write(f"JOB:        {I.GET_JOB()}\n")
                    F.write(f"TUITION:    {I.GET_TUT()}\n")
                    F.write(f"LOAN:       {I.GET_LON()} (avg.)\n")
                    F.write(f"REPAY IN:   {I.GET_MTH_PAY()} months (est.)\n")
                    F.write(f"{Control.DSH('')}\n")
                F.close()

if __name__ == "__main__":
    Control.main()