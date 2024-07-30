import sys
import os
import re
from typing import List
from datetime import datetime
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from CTree import CTree
from Manager import Manager
from Styles import Styles

class CareerTree(QMainWindow):

    class DynamicButton(QPushButton):
        def __init__(self, TXT_1: str, TXT_2: str, parent=None):
            super().__init__(parent)
            self.setMouseTracking(True)
            self.setText(TXT_1)
            self.installEventFilter(self)
            self.TXT_1 = TXT_1
            self.TXT_2 = TXT_2

        def eventFilter(self, obj, event):
            if obj is self:
                if event.type() == QEvent.Type.Enter:
                    self.setFixedSize(8 * len(self.TXT_2) + 24, 30)
                    self.setText(self.TXT_2)
                elif event.type() == QEvent.Type.Leave:
                    self.setFixedSize(8 * len(self.TXT_1) + 24, 30)
                    self.setText(self.TXT_1)
            return super().eventFilter(obj, event)

    class TextDialog(QDialog):
        def __init__(self, TXT: str, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Career Tree & College Report")
            self.setGeometry(100, 100, 600, 400)
            self.setWindowIcon(QIcon('resources/icon_full_borderless_shadow_dark'))

            layout = QVBoxLayout(self)

            self.TXT_MAIN = QTextEdit()
            self.TXT_MAIN.setReadOnly(True)
            self.TXT_MAIN.setMarkdown(TXT)
            layout.addWidget(self.TXT_MAIN)

            BUT_OK = QPushButton("OK")
            BUT_OK.clicked.connect(self.accept)
            layout.addWidget(BUT_OK)
            
            self.setStyleSheet(Styles.MISC_0)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Career Tree")
        self.setGeometry(50, 50, 900, 600)
        self.setWindowIcon(QIcon('resources/icon_full_borderless_shadow'))

        self.WGT_CTR = QWidget()
        self.setCentralWidget(self.WGT_CTR)
        
        LAY_MAIN = QVBoxLayout(self.WGT_CTR)
        
        WGT_TOP = QWidget()
        LAY_TOP = QHBoxLayout(WGT_TOP)
        
        self.BUT_TOP = {
            'QUIT': QPushButton('Quit'),
            'EXP': self.DynamicButton('Export', 'Export Tree, Report, and Summary!'),
            'INS': QPushButton('In-State'),
            'SIZE': QPushButton('Size of Career Options'),
            'THEME': QPushButton('Theme'),
        }
        
        self.BUT_TOP['QUIT'].setFixedSize(8 * len(self.BUT_TOP['QUIT'].text()) + 24, 30)
        self.BUT_TOP['EXP'].setFixedSize(8 * len(self.BUT_TOP['EXP'].text()) + 24, 30)
        # SPACER
        self.BUT_TOP['INS'].setFixedSize(8 * len(self.BUT_TOP['INS'].text()) + 24, 30)
        self.BUT_TOP['SIZE'].setFixedSize(8 * len(self.BUT_TOP['SIZE'].text()) + 24, 30)
        self.BUT_TOP['THEME'].setFixedSize(8 * len(self.BUT_TOP['THEME'].text()) + 24, 30)
        
        for i, BUT_TOP in enumerate(self.BUT_TOP.values()):
            if i == 2:
                LAY_TOP.addStretch(1)
            LAY_TOP.addWidget(BUT_TOP)
            BUT_TOP.clicked.connect(self.BUT_CLICK)

        LAY_MAIN.addWidget(WGT_TOP)

        self.TXT_MAIN = QTextEdit()
        self.TXT_MAIN.setReadOnly(True)
        LAY_MAIN.addWidget(self.TXT_MAIN)

        self.BUT = {
            'LOC': QPushButton('Location -> Career -> Job -> College (START HERE!)'),
            'CAR': QPushButton('Career -> Job -> College'),
            'JOB': QPushButton('Job -> College'),
            'COL': QPushButton('College'),
            'INFO': QPushButton('Info (Description of Selected College)'),
            'VIEW': QPushButton('View (Career Tree and College Report)'),
            'AI': QPushButton('AI (custom question)'),
        }

        for BUT in self.BUT.values():
            BUT.setFixedHeight(30)
            LAY_MAIN.addWidget(BUT)
            BUT.clicked.connect(self.BUT_CLICK)

        self.BUT['CAR'].setEnabled(False)
        self.BUT['JOB'].setEnabled(False)
        self.BUT['COL'].setEnabled(False)
        self.BUT['INFO'].setEnabled(False)
        self.BUT['VIEW'].setEnabled(False)

        self.ALT_THEME = 0
        self.setStyleSheet(Styles.LGHT)

        self.MGR = Manager(10, 1) # DEF : X = 10 , IN-STATE
        self.CAREER_TREE = CTree()
        self.COLLEGE_INFO: List[Manager.College_Info] = []

        self.initialize_app()

    def initialize_app(self):
        self.STR_DT = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
        self.X = 18
        self.INS = 1
        self.MGR.__init__(self.X, self.INS)
        self.PRINT("""**Welcome to the Career Tree!**<br/><br/>Start by adding a location and completing a branch. Continue exploring career options from there!<br/><br/><em>Example starter tree:</em><br/><em>LOC USA</em><br/> <em>└── CAR Software Developer</em><br/>     <em>└── JOB Cybersecurity Specialist</em><br/>           <em>└── COL North Carolina State University</em>""")

    ################################################################

    def BUT_CLICK(self):
        SDR = self.sender()
        CMD = SDR.text().split()[0].lower()
        _LOC_ = False

        if CMD == 'location':
            self.BUT['CAR'].setEnabled(False)
            self.BUT['JOB'].setEnabled(False)
            self.BUT['COL'].setEnabled(False)
            self.BUT['INFO'].setEnabled(False)
            self.BUT['VIEW'].setEnabled(False)
            _LOC_ = self.CMD_LOC()
            if _LOC_:
                self.BUT['CAR'].setEnabled(True)
                self.BUT['JOB'].setEnabled(True)
                self.BUT['COL'].setEnabled(True)
                self.BUT['INFO'].setEnabled(True)
                self.BUT['VIEW'].setEnabled(True)
                self.BUT['LOC'].setText('Location -> Career -> Job -> College (RESET TREE!)')
                self.BUT['CAR'].setText(f'Career -> Job -> College (Explore a career in {self.MGR.GET('LOC')})')
                self.BUT['JOB'].setText(f'Job -> College (Explore a job in the {self.MGR.GET('CAR')} career)')
                self.BUT['COL'].setText(f'College (Explore a college for a {self.MGR.GET('JOB')} job)')
        elif CMD == 'career':
            self.CMD_CAR()
        elif CMD == 'job':
            self.CMD_JOB()
        elif CMD == 'college':
            self.CMD_COL()
        elif CMD == 'info':
            self.CMD_INFO()
        elif CMD == 'view':
            self.CMD_VIEW()
        elif CMD == 'ai':
            self.CMD_AI()
        elif CMD == 'quit':
            self.CMD_QUIT()
        elif CMD == 'export':
            self.CMD_EXP()
        elif CMD == 'in-state':
            self.CMD_INS()
        elif CMD == 'size':
            self.CMD_SIZE()
        elif CMD == 'theme':
            self.CMD_THEME()

    def CMD_LOC(self):
        LOC, ok = QInputDialog.getText(self, "Location", "Enter your current / desired location:")
        if ok:
            if LOC != '':
                # LOCX = self.MGR.GET_DBG_GPT(f"ANSWER WITH ONLY 1 LETTER (Y/N): does {LOC} contain a valid location?").lower() == 'y'
                # if not LOCX:
                    # LOC = "USA"
                # else:
                LOCS = self.MGR.GET_DBG_GPT("ANSWER WITH ONLY 1 LETTER (Y/N): is {LOC} a single location?").lower() == 'n'
                if LOCS:
                    LOC = self.MGR.GET_DBG_GPT(f"NO EXTRA DESCRIPTION: list the locations '{LOC}' AS A '|' SEPARATED LIST, replacing invalid locations with USA")
                    LOC = self.MGR.GET_DBG_GPT(f"NO EXTRA DESCRIPTION: if {LOC} contains any duplicates, remove them and print the list, else print the unchanged list, DO NOT CHANGE THE FORMATTING").replace('|', ', ')
            else:
                LOC = "USA"
            LOC_ADD = ' '.join([W.title() if W.islower() else W for W in LOC.split()])
            self.MGR.SET('LOC', LOC_ADD)

            CAR_ADD = self.PARSE("Choose a Career", "CAR")
            JOB_ADD = self.PARSE("Choose a Job", "JOB")
            COL_ADD = self.PARSE("Choose a College", "COL")

            self.CAREER_TREE.ADD(0, LOC_ADD, CAR_ADD, JOB_ADD, COL_ADD)
            self.CAREER_TREE.ADD(1, LOC_ADD, CAR_ADD, JOB_ADD, COL_ADD)
            self.CAREER_TREE.ADD(2, LOC_ADD, CAR_ADD, JOB_ADD, COL_ADD)

            if self.CAREER_TREE.ADD(3, LOC_ADD, CAR_ADD, JOB_ADD, COL_ADD):
                INF = self.MGR.GET_COL_INF_GPT()
                if INF:
                    self.COLLEGE_INFO = [INF]
                CAREER_TREE_STR = """─""" * 32 + """<br/>""" + self.CAREER_TREE.STR() + """<br/>""" + """─""" * 32;
                self.PRINT(f"""*Branch added.*<br/><br/>Career Tree:<br/>{CAREER_TREE_STR}""")
            else:
                self.PRINT("""*Branch selected.*""")
                CAREER_TREE_STR = """─""" * 32 + """<br/>""" + self.CAREER_TREE.STR() + """<br/>""" + """─""" * 32;
                self.PRINT(f"""*Branch selected.*<br/><br/>Career Tree:<br/>{CAREER_TREE_STR}""")
            return True
        return False

    def CMD_CAR(self):
        CAR_ADD = self.PARSE("Choose a Career", "CAR")
        JOB_ADD = self.PARSE("Choose a Job", "JOB")
        COL_ADD = self.PARSE("Choose a College", "COL")

        self.CAREER_TREE.ADD(1, self.MGR.GET('LOC'), CAR_ADD, JOB_ADD, COL_ADD)
        self.CAREER_TREE.ADD(2, self.MGR.GET('LOC'), CAR_ADD, JOB_ADD, COL_ADD)

        if self.CAREER_TREE.ADD(3, self.MGR.GET('LOC'), CAR_ADD, JOB_ADD, COL_ADD):
            INF = self.MGR.GET_COL_INF_GPT()
            if INF:
                self.COLLEGE_INFO.append(INF)
            CAREER_TREE_STR = """─""" * 32 + """<br/>""" + self.CAREER_TREE.STR() + """<br/>""" + """─""" * 32;
            self.PRINT(f"""*Branch added.*<br/><br/>Career Tree:<br/>{CAREER_TREE_STR}""")
        else:
            self.PRINT("""*Branch selected.*""")
            CAREER_TREE_STR = """─""" * 32 + """<br/>""" + self.CAREER_TREE.STR() + """<br/>""" + """─""" * 32;
            self.PRINT(f"""*Branch selected.*<br/><br/>Career Tree:<br/>{CAREER_TREE_STR}""")

    def CMD_JOB(self):
        JOB_ADD = self.PARSE("Choose a Job", "JOB")
        COL_ADD = self.PARSE("Choose a College", "COL")

        self.CAREER_TREE.ADD(2, self.MGR.GET('LOC'), self.MGR.GET('CAR'), JOB_ADD, COL_ADD)

        if self.CAREER_TREE.ADD(3, self.MGR.GET('LOC'), self.MGR.GET('CAR'), JOB_ADD, COL_ADD):
            INF = self.MGR.GET_COL_INF_GPT()
            if INF:
                self.COLLEGE_INFO.append(INF)
            CAREER_TREE_STR = """─""" * 32 + """<br/>""" + self.CAREER_TREE.STR() + """<br/>""" + """─""" * 32;
            self.PRINT(f"""*Branch added.*<br/><br/>Career Tree:<br/>{CAREER_TREE_STR}""")
        else:
            self.PRINT("""*Branch selected.*""")
            CAREER_TREE_STR = """─""" * 32 + """<br/>""" + self.CAREER_TREE.STR() + """<br/>""" + """─""" * 32;
            self.PRINT(f"""*Branch selected.*<br/><br/>Career Tree:<br/>{CAREER_TREE_STR}""")

    def CMD_COL(self):
        COL_ADD = self.PARSE("Choose a College", "COL")

        if self.CAREER_TREE.ADD(3, self.MGR.GET('LOC'), self.MGR.GET('CAR'), self.MGR.GET('JOB'), COL_ADD):
            INF = self.MGR.GET_COL_INF_GPT()
            if INF:
                self.COLLEGE_INFO.append(INF)
            CAREER_TREE_STR = """─""" * 32 + """<br/>""" + self.CAREER_TREE.STR() + """<br/>""" + """─""" * 32;
            self.PRINT(f"""*Branch added.*<br/><br/>Career Tree:<br/>{CAREER_TREE_STR}""")
        else:
            self.PRINT("""*Branch selected.*""")
            CAREER_TREE_STR = """─""" * 32 + """<br/>""" + self.CAREER_TREE.STR() + """<br/>""" + """─""" * 32;
            self.PRINT(f"""*Branch selected.*<br/><br/>Career Tree:<br/>{CAREER_TREE_STR}""")

    def CMD_INFO(self):
        DESC = self.MGR.GET_COL_DSC_GPT()
        self.PRINT(f"""**College Information:**<br/>{DESC}""")

    def CMD_VIEW(self):
        CAREER_TREE_STR = """─""" * 32 + """<br/>""" + self.CAREER_TREE.STR() + """<br/>""" + """─""" * 32;
        self.PRINT(f"""<br/>Career Tree:<br/>{CAREER_TREE_STR}""")
        COLLEGE_REPORT_STR = self.GET_COLLEGE_REPORT()
        BOX_VIEW = self.TextDialog(f"""Career Tree:<br/>{CAREER_TREE_STR}<br/><br/>College Report:<br/>{COLLEGE_REPORT_STR}""")
        BOX_VIEW.exec()

    def CMD_AI(self):
        QST, ok = QInputDialog.getText(self, "AI Question", "Enter your question:")
        if ok:
            if QST == '':
                self.PRINT("""**Answer:**   Please ask a related question.""")
            else:
                ANS = self.MGR.GET_EXT_GPT(QST)
                self.PRINT(f"""**Question:** {QST.capitalize() + '.'}<br/>**Answer:**   {ANS}""")

    def CMD_QUIT(self):
        QApplication.quit()

    def CMD_EXP(self):
        if self.MGR.GET('CAR') is not None:
            self.EXPORT()

    def CMD_INS(self):
        self.INS = -1 * (self.INS - 1)
        self.MGR.SET_INS(self.INS)
        INS_STR = "In-state" if self.INS == 1 else "In-state and Out-of-state"
        self.BUT_TOP['INS'].setText(INS_STR)
        self.BUT_TOP['INS'].setFixedSize(8 * len(self.BUT_TOP['INS'].text()) + 30, 30)

    def CMD_SIZE(self):
        X_INP, ok = QInputDialog.getInt(self, "List size", f"Size of list responses from AI? Current: {self.X}", 18, 4, 36)
        if ok:
            self.X = X_INP
            self.MGR.SET_X(self.X)

    def CMD_THEME(self):
        if self.ALT_THEME == 0:
            self.setWindowIcon(QIcon('resources/icon_full_borderless_shadow_alt'))
            self.setStyleSheet(Styles.DARK)
            self.ALT_THEME = 1
        elif self.ALT_THEME == 1:
            self.setWindowIcon(QIcon('resources/icon_full_borderless_shadow_dark'))
            self.setStyleSheet(Styles.NGHT)
            self.ALT_THEME = 2
        else:
            self.setWindowIcon(QIcon('resources/icon_full_borderless_shadow'))
            self.setStyleSheet(Styles.LGHT)
            self.ALT_THEME = 0

    ################################################################

    def PARSE(self, QST, TYP):
        OPT = self.MGR.GET_CAR_GPT() if TYP == "CAR" else self.MGR.GET_JOB_GPT() if TYP == "JOB" else self.MGR.GET_COL_GPT()
        OPT = re.sub(r'[0-9]+', '', OPT).replace(' .', '.').replace('. ', '.').replace('.', '').replace(' |', '|').replace('| ', '|').replace('\n', '|').replace('||', '|')
        OPT = OPT.split('|')
        XYZ, ok = QInputDialog.getItem(self, QST, "Select an option:", OPT, 0, False)
        if not ok:
            XYZ = OPT[0]
        if TYP == "CAR":
            self.MGR.SET('CAR', XYZ)
        elif TYP == "JOB":
            self.MGR.SET('JOB', XYZ)
            self.MGR.GET_PAY_GPT()
        elif TYP == "COL":
            self.MGR.SET('COL', XYZ)
            self.MGR.GET_DEG_GPT()
        return XYZ

    def PRINT(self, MSG):
        self.TXT_MAIN.setMarkdown(MSG)
        self.TXT_MAIN.moveCursor(QTextCursor.MoveOperation.End)

    def GET_COLLEGE_REPORT(self):
        if not self.COLLEGE_INFO:
            return """No colleges"""
        STR = """─""" * 32 + """<br/>"""
        for i in self.COLLEGE_INFO:
            STR += (
                f"""NAME:       {i.GET('COL')}<br/>"""
                f"""LOCATION:   {i.GET('LOC')}<br/>"""
                f"""DEGREE:     {i.GET('DEG')}<br/>"""
                f"""REQS:       {i.GET('REQ')}<br/>"""
                f"""CAREER:     {i.GET('CAR')}<br/>"""
                f"""JOB:        {i.GET('JOB')}<br/>"""
                f"""PAY ENTRY:  {i.GET('PAY_LOW')}<br/>"""
                f"""PAY SENIOR: {i.GET('PAY_UPP')}<br/>"""
                f"""TUITION:    {i.GET('TUT')}<br/>"""
                f"""LOAN:       {i.GET('LON')} (avg.)<br/>"""
                f"""REPAY IN:   {i.GET_MTH_PAY()} months (est.)<br/>"""
            )
            STR += """─""" * 32 + """<br/>"""
        return STR

    def EXPORT(self):
        PATH = os.path.join(os.path.normpath(os.path.expanduser("~/Desktop")), "output")
        if not os.path.exists(PATH):
            os.makedirs(PATH)

        if not os.path.exists(os.path.join(PATH, self.STR_DT)):
            os.makedirs(os.path.join(PATH, self.STR_DT))

        F_CAREER_TREE_STR = f"Tree_{self.STR_DT}.txt"
        PATH_CAREER_TREE = os.path.join(os.path.join(PATH, self.STR_DT), F_CAREER_TREE_STR)
        with open(PATH_CAREER_TREE, 'w', encoding="utf-8") as F:
            F.write(f"{'─' * 32}\n{self.CAREER_TREE.STR().replace("<br/>", '\n')}\n{'─' * 32}")

        if self.COLLEGE_INFO:
            F_COLLEGE_REPORT_STR = f"Report_{self.STR_DT}.txt"
            PATH_COLLEGE_REPORT = os.path.join(os.path.join(PATH, self.STR_DT), F_COLLEGE_REPORT_STR)
            with open(PATH_COLLEGE_REPORT, 'w', encoding="utf-8") as F:
                F.write(self.GET_COLLEGE_REPORT().replace("<br/>", '\n'))

        F_CAREER_SUMMARY_STR = f"Summary_{self.STR_DT}.txt"
        PATH_CAREER_SUMMARY = os.path.join(os.path.join(PATH, self.STR_DT), F_CAREER_SUMMARY_STR)
        with open(PATH_CAREER_SUMMARY, 'w', encoding="utf-8") as F:
            SUMMARY = self.MGR.GET_SUM_GPT(self.CAREER_TREE)
            F.write(SUMMARY)
            self.PRINT(SUMMARY + f"""<br/><br/>*Exported Career Tree, College Report, and Summary to {PATH}*""")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CareerTree()
    window.show()
    sys.exit(app.exec())