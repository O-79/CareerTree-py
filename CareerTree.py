import sys
import os
import re
from typing import List
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from CTree import CTree
from Manager import Manager
from datetime import datetime
from Styles import Styles

class CareerTree(QMainWindow):
    ALT_THEME = 0;
    
    class TextDialog(QDialog):
        def __init__(self, text, parent = None):
            super().__init__(parent)
            self.setWindowTitle("Career Tree & College Report")
            self.setGeometry(100, 100, 600, 400)
            self.setWindowIcon(QIcon('resources/icon_full_borderless_shadow_dark'))

            layout = QVBoxLayout(self)

            self.TXT_MAIN = QTextEdit()
            self.TXT_MAIN.setReadOnly(True)
            self.TXT_MAIN.setMarkdown(text)
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
            'EXP': QPushButton('Export'),
            'INS': QPushButton('Colleges'),
            'SIZE': QPushButton('Size'),
            'THEME': QPushButton('Theme'),
        }
        
        self.BUT_TOP['QUIT'].setFixedSize(55, 30)
        self.BUT_TOP['EXP'].setFixedSize(70, 30)
        # SPACER
        self.BUT_TOP['INS'].setFixedSize(90, 30)
        self.BUT_TOP['SIZE'].setFixedSize(55, 30)
        self.BUT_TOP['THEME'].setFixedSize(65, 30)
        
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
            'LOC': QPushButton('Location (add and reset tree)'),
            'CAR': QPushButton('Career (add / select existing)'),
            'JOB': QPushButton('Job (add / select existing)'),
            'COL': QPushButton('College (add / select existing)'),
            'INFO': QPushButton('Info (current college description)'),
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
        
        self.setStyleSheet(Styles.LGHT)

        self.MGR = Manager(10, 1) # DEF : X = 10 , IN-STATE
        self.CAREER_TREE = CTree()
        self.COLLEGE_INFO: List[Manager.College_Info] = []

        self.initialize_app()

    def initialize_app(self):
        self.STR_DT = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
        self.MGR.__init__(10, 1)
        self.MGR.SET('LOC', "United States of America")
        self.PRINT("""**Welcome to the** <a href='https://github.com/O-79/CareerTree-py/'><b>Career Tree!</b></a>""") # FIX

    ################################################################

    def BUT_CLICK(self):
        SDR = self.sender()
        CMD = SDR.text().split()[0].lower()

        if CMD == 'location':
            self.CMD_LOC()
            self.BUT['CAR'].setEnabled(True)
            self.BUT['JOB'].setEnabled(True)
            self.BUT['COL'].setEnabled(True)
            self.BUT['INFO'].setEnabled(True)
            self.BUT['VIEW'].setEnabled(True)
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
        elif CMD == 'export':
            self.CMD_EXP()
        elif CMD == 'quit':
            self.CMD_QUIT()
        elif CMD == 'colleges':
            self.CMD_INS()
        elif CMD == 'size':
            self.CMD_SIZE()
        elif CMD == 'theme':
            self.CMD_THEME()

    def CMD_LOC(self):
        ok = False
        while not ok:
            LOC, ok = QInputDialog.getText(self, "Location", "Enter your current / desired location:")
        
        if LOC == '':
            LOC = "United States of America"
        LOC_ADD = LOC[0].upper() + LOC[1:]
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
            self.PRINT("""*Branch added.*""")
        else:
            self.PRINT("""*Branch selected.*""")

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
            self.PRINT("""*Branch added.*""")
        else:
            self.PRINT("""*Branch selected.*""")

    def CMD_JOB(self):
        JOB_ADD = self.PARSE("Choose a Job", "JOB")
        COL_ADD = self.PARSE("Choose a College", "COL")

        self.CAREER_TREE.ADD(2, self.MGR.GET('LOC'), self.MGR.GET('CAR'), JOB_ADD, COL_ADD)

        if self.CAREER_TREE.ADD(3, self.MGR.GET('LOC'), self.MGR.GET('CAR'), JOB_ADD, COL_ADD):
            INF = self.MGR.GET_COL_INF_GPT()
            if INF:
                self.COLLEGE_INFO.append(INF)
            self.PRINT("""*Branch added.*""")
        else:
            self.PRINT("""*Branch selected.*""")

    def CMD_COL(self):
        COL_ADD = self.PARSE("Choose a College", "COL")

        if self.CAREER_TREE.ADD(3, self.MGR.GET('LOC'), self.MGR.GET('CAR'), self.MGR.GET('JOB'), COL_ADD):
            INF = self.MGR.GET_COL_INF_GPT()
            if INF:
                self.COLLEGE_INFO.append(INF)
            self.PRINT("""*Branch added.*""")
        else:
            self.PRINT("""*Branch selected.*""")

    def CMD_INFO(self):
        DESC = self.MGR.GET_COL_DSC_GPT()
        self.PRINT(f"""**College Information:**
                               <br/>{DESC}""")

    def CMD_VIEW(self):
        tree_str = self.CAREER_TREE.STR()
        college_report = self.get_college_report()
        dialog_view = self.TextDialog(f"""Career Tree:
                                          <br/>{tree_str}
                                          <br/><br/>College Report:
                                          <br/>{college_report}""")
        dialog_view.exec()

    def CMD_AI(self):
        QST, ok = QInputDialog.getText(self, "AI Question", "Enter your question:")
        if ok:
            if QST == '':
                self.PRINT("""**Answer:**   Please ask a related question.""")
            else:
                ANS = self.MGR.GET_EXT_GPT(QST)
                self.PRINT(f"""**Question:** {QST.capitalize() + '.'}
                                       <br/>**Answer:**   {ANS}""")

    def CMD_EXP(self):
        if self.MGR.GET('CAR') is not None:
            self.EXPORT()

    def CMD_QUIT(self):
        QApplication.quit()

    def CMD_INS(self):
        INS_ANS = QMessageBox.question(self, "In-State / Out-of-State", "Include out-of-state colleges?",
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        self.INS = 0 if INS_ANS == QMessageBox.StandardButton.Yes else 1
        self.MGR.SET_INS(self.INS)

    def CMD_SIZE(self):
        self.X = QInputDialog.getInt(self, "List size", "Size of list responses from AI? [4 (Faster) - 16 (Slower)]", 10, 4, 16)
        self.MGR.SET_X(self.X)

    def CMD_THEME(self):
        global ALT_THEME
        if self.ALT_THEME == 0:
            self.setWindowIcon(QIcon('resources/icon_full_borderless_shadow_alt'))
            self.setStyleSheet(Styles.DARK)
            self.ALT_THEME = 1
        else:
            self.setWindowIcon(QIcon('resources/icon_full_borderless_shadow'))
            self.setStyleSheet(Styles.LGHT)
            self.ALT_THEME = 0

    ################################################################

    def PARSE(self, QST, TYP):
        OPT = self.MGR.GET_CAR_GPT() if TYP == "CAR" else self.MGR.GET_JOB_GPT() if TYP == "JOB" else self.MGR.GET_COL_GPT()
        OPT = re.sub(r'[0-9]+', '', OPT).replace(' .', '.').replace('. ', '.').replace('.', '').replace(' |', '|').replace('| ', '|').replace('\n', '|').replace('||', '|')
        OPT = OPT.split('|')
        ok = False
        while not ok:
            XYZ, ok = QInputDialog.getItem(self, QST, "Select an option:", OPT, 0, False)
        if ok:
            if TYP == "CAR":
                self.MGR.SET('CAR', XYZ)
            elif TYP == "JOB":
                self.MGR.SET('JOB', XYZ)
                self.MGR.GET_PAY_GPT()
            elif TYP == "COL":
                self.MGR.SET('COL', XYZ)
                self.MGR.GET_DEG_GPT()
            return XYZ
        return None

    def PRINT(self, MSG):
        self.TXT_MAIN.setMarkdown(MSG)
        self.TXT_MAIN.moveCursor(QTextCursor.MoveOperation.End)

    def get_college_report(self):
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
        path = os.path.join(os.path.normpath(os.path.expanduser("~/Desktop")), "output")
        if not os.path.exists(path):
            os.makedirs(path)

        if not os.path.exists(os.path.join(path, self.STR_DT)):
            os.makedirs(os.path.join(path, self.STR_DT))

        f_name_ctree = f"Tree_{self.STR_DT}.txt"
        PATH_CTREE = os.path.join(os.path.join(path, self.STR_DT), f_name_ctree)
        with open(PATH_CTREE, 'w', encoding="utf-8") as f:
            f.write(f"{'─' * 32}\n{self.CAREER_TREE.STR().replace("<br/>", '\n')}\n{'─' * 32}")

        if self.COLLEGE_INFO:
            f_name_colrep = f"Report_{self.STR_DT}.txt"
            path_COLREP = os.path.join(os.path.join(path, self.STR_DT), f_name_colrep)
            with open(path_COLREP, 'w', encoding="utf-8") as f:
                f.write(self.get_college_report().replace("<br/>", '\n'))

        self.PRINT(f"""*Exported Career Tree & College Report to {path}*""")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CareerTree()
    window.show()
    sys.exit(app.exec())