from typing import List
from CTree import CTree
from Manager import Manager  # Assuming MGR is another module/class

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

        print(f"* Choose (1 - {X}):\n{XYZ}")
        try:
            SEL = int(input())
        except ValueError:
            SEL = 1

        if SEL < 1:
            SEL = 1
        if SEL > X:
            SEL = X
        
        print(SEL)

        XYZ_SEL = XYZ.split(',')[SEL - 1].strip()

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

        LOC_ADD = input()
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
        MGR = Manager();
        CAREER_TREE = CTree()
        COLLEGE_INFO: List[Manager.College_Info] = []

        X = 10
        print(Control.Q_SIZ)
        try:
            X = int(input())
            if X < 4:
                X = 4
            if X > 16:
                X = 16
            MGR.INIT(X)
        except ValueError:
            MGR.INIT(X)

        Control.TMP = X

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
            print(f"CAREER:     {I.GET_CAR()}")
            print(f"JOB:        {I.GET_JOB()}")
            print(f"TUITION:    {I.GET_TUT()}")
            print(f"LOAN:       {I.GET_LON()}")
            print(f"PROGRAMS:   {I.GET_LON_OPP()}")
            print(f"REPAY IN:   {I.GET_MTH_PAY()} months")
            print(Control.DSH(''))

if __name__ == "__main__":
    Control.main()