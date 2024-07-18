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

class CareerTreeGUI(QMainWindow):
    ALT_THEME = 0;
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Career Tree")
        self.setGeometry(100, 100, 900, 600)
        self.setWindowIcon(QIcon('icon_full_borderless_shadow_v1.1'))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        main_layout = QVBoxLayout(self.central_widget)
        
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        top_layout.addStretch(1)
        
        self.theme_button = QPushButton('[Theme]')
        self.theme_button.setFixedSize(75, 30)
        top_layout.addWidget(self.theme_button)
        self.theme_button.clicked.connect(self.handle_button_click)

        main_layout.addWidget(top_widget)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        main_layout.addWidget(self.output_text)
        
        self.set_style_light()

        self.buttons = {
            'LOC': QPushButton('Location (add)'),
            'CAR': QPushButton('Career (add / select existing)'),
            'JOB': QPushButton('Job (add / select existing)'),
            'COL': QPushButton('College (add / select existing)'),
            'INFO': QPushButton('Info (current college description)'),
            'VIEW': QPushButton('View (Career Tree and College Report)'),
            'AI': QPushButton('AI (custom question)'),
            'QUIT': QPushButton('Quit (and export)')
        }

        for button in self.buttons.values():
            button.setFixedHeight(30)
            main_layout.addWidget(button)
            button.clicked.connect(self.handle_button_click)

        self.buttons['CAR'].setEnabled(False)
        self.buttons['JOB'].setEnabled(False)
        self.buttons['COL'].setEnabled(False)
        self.buttons['INFO'].setEnabled(False)
        self.buttons['VIEW'].setEnabled(False)

        self.mgr = Manager()
        self.career_tree = CTree()
        self.college_info: List[Manager.College_Info] = []

        self.initialize_app()

    def initialize_app(self):
        ok = False
        while not ok:
            self.x, ok = QInputDialog.getInt(self, "List size", "Size of list responses from AI ? [4 (Faster) - 16 (Slower)]", 10, 4, 16)

        ins_response = QMessageBox.question(self, "Out-of-State Colleges", "Are you interested in out-of-state colleges?",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        self.ins = 0 if ins_response == QMessageBox.StandardButton.Yes else 1

        self.mgr.INIT(self.x, self.ins)
        self.mgr.SET_LOC("United States of America")
        self.print_message(self.get_menu())

    def handle_button_click(self):
        sender = self.sender()
        command = sender.text().split()[0].lower()

        if command == 'location':
            self.cmd_loc()
            self.buttons['CAR'].setEnabled(True)
            self.buttons['JOB'].setEnabled(True)
            self.buttons['COL'].setEnabled(True)
            self.buttons['INFO'].setEnabled(True)
            self.buttons['VIEW'].setEnabled(True)
        elif command == 'career':
            self.cmd_car()
        elif command == 'job':
            self.cmd_job()
        elif command == 'college':
            self.cmd_col()
        elif command == 'info':
            self.cmd_info()
        elif command == 'view':
            self.cmd_view()
        elif command == 'ai':
            self.cmd_ai()
        elif command == 'quit':
            self.cmd_quit()
        elif command == '[theme]':
            global ALT_THEME
            if self.ALT_THEME == 0:
                self.setWindowIcon(QIcon('icon_full_borderless_shadow_alt_v1.1'))
                self.set_style_dark()
                self.ALT_THEME = 1
            else:
                self.setWindowIcon(QIcon('icon_full_borderless_shadow_v1.1'))
                self.set_style_light()
                self.ALT_THEME = 0

    def cmd_loc(self):
        ok = False
        while not ok:
            loc, ok = QInputDialog.getText(self, "Location", "Enter your current / desired location:")
        if ok:
            if loc == '':
                loc = "United States of America"
            loc_add = loc[0].upper() + loc[1:]
            self.mgr.SET_LOC(loc_add)

            car_add = self.parse_and_get_input("Choose a Career", "CAR")
            job_add = self.parse_and_get_input("Choose a Job", "JOB")
            col_add = self.parse_and_get_input("Choose a College", "COL")

            self.career_tree.ADD(0, loc_add, car_add, job_add, col_add)
            self.career_tree.ADD(1, loc_add, car_add, job_add, col_add)
            self.career_tree.ADD(2, loc_add, car_add, job_add, col_add)

            if self.career_tree.ADD(3, loc_add, car_add, job_add, col_add):
                inf = self.mgr.GET_COL_INF_GPT()
                if inf:
                    self.college_info = [inf]
                self.print_message("Location and related information added successfully.")
            else:
                self.print_message("Failed to add location and related information.")

    def cmd_car(self):
        car_add = self.parse_and_get_input("Choose a Career", "CAR")
        job_add = self.parse_and_get_input("Choose a Job", "JOB")
        col_add = self.parse_and_get_input("Choose a College", "COL")

        self.career_tree.ADD(1, self.mgr.GET_LOC(), car_add, job_add, col_add)
        self.career_tree.ADD(2, self.mgr.GET_LOC(), car_add, job_add, col_add)

        if self.career_tree.ADD(3, self.mgr.GET_LOC(), car_add, job_add, col_add):
            inf = self.mgr.GET_COL_INF_GPT()
            if inf:
                self.college_info.append(inf)
            self.print_message("Career and related information added successfully.")
        else:
            self.print_message("Failed to add career and related information.")

    def cmd_job(self):
        job_add = self.parse_and_get_input("Choose a Job", "JOB")
        col_add = self.parse_and_get_input("Choose a College", "COL")

        self.career_tree.ADD(2, self.mgr.GET_LOC(), self.mgr.GET_CAR(), job_add, col_add)

        if self.career_tree.ADD(3, self.mgr.GET_LOC(), self.mgr.GET_CAR(), job_add, col_add):
            inf = self.mgr.GET_COL_INF_GPT()
            if inf:
                self.college_info.append(inf)
            self.print_message("Job and related information added successfully.")
        else:
            self.print_message("Failed to add job and related information.")

    def cmd_col(self):
        col_add = self.parse_and_get_input("Choose a College", "COL")

        if self.career_tree.ADD(3, self.mgr.GET_LOC(), self.mgr.GET_CAR(), self.mgr.GET_JOB(), col_add):
            inf = self.mgr.GET_COL_INF_GPT()
            if inf:
                self.college_info.append(inf)
            self.print_message("College information added successfully.")
        else:
            self.print_message("Failed to add college information.")

    def cmd_info(self):
        info = self.mgr.GET_COL_DSC_GPT()
        self.print_message(f"College Information:\n{info}")

    def cmd_view(self):
        tree_str = self.career_tree.STR()
        college_report = self.get_college_report()
        self.print_message(f"Career Tree:\n{tree_str}\n\nCollege Report:\n{college_report}")

    def cmd_ai(self):
        question, ok = QInputDialog.getText(self, "AI Question", "Enter your question:")
        if ok:
            if question == '':
                self.print_message("Answer: Please ask a related question.")
            else:
                answer = self.mgr.GET_EXT_GPT(question)
                self.print_message(f"Question: {question}\nAnswer: {answer}")

    def cmd_quit(self):
        if self.mgr.GET_CAR() is not None:
            self.export_data()
        QApplication.quit()

    def parse_and_get_input(self, prompt, typ):
        options = self.mgr.GET_CAR_GPT() if typ == "CAR" else self.mgr.GET_JOB_GPT() if typ == "JOB" else self.mgr.GET_COL_GPT()
        options = re.sub(r'[0-9]+', '', options).replace(' .', '.').replace('. ', '.').replace('.', '').replace(' |', '|').replace('| ', '|').replace('\n', '|').replace('||', '|')
        options = options.split('|')
        ok = False
        while not ok:
            item, ok = QInputDialog.getItem(self, prompt, "Select an option:", options, 0, False)
        if ok:
            if typ == "CAR":
                self.mgr.SET_CAR(item)
            elif typ == "JOB":
                self.mgr.SET_JOB(item)
            elif typ == "COL":
                self.mgr.SET_COL(item)
            return item
        return None

    def print_message(self, message):
        self.output_text.append("\n" + message)
        self.output_text.moveCursor(QTextCursor.MoveOperation.End)

    def get_menu(self):
        return (
            "WELCOME TO THE CAREER TREE\n"
            "USING: gpt-3.5-turbo\n"
            "CMD MENU\n"
            "'LOC' / 'l'  →  [RESETS TREE]              & Create a new full branch   with a location, career, job, college\n"
            "'CAR' / 'c'  →  Select an existing career  / Create a new long branch   with a career, job, college\n"
            "'JOB' / 'j'  →  Select an existing job     / Create a new medium branch with a job, college\n"
            "'COL' / 'u'  →  Select an existing college / Create a new short branch  with a college\n"
            "'INFO' / 'i' →  More information about currently selected college\n"
            "'VIEW' / 'v' →  View current Career Tree & College Report\n"
            "'AI'         →  Ask a custom but related question\n"
            "'QUIT' / 'q' →  Export Career Tree & College Report, exit application\n"
        )

    def get_college_report(self):
        if not self.college_info:
            return "No colleges"
        report = "─" * 32 + "\n"
        for i in self.college_info:
            report += (
                f"NAME:       {i.GET_COL()}\n"
                f"LOCATION:   {i.GET_LOC()}\n"
                f"DEGREE:     {i.GET_DEG()}\n"
                f"REQS:       {i.GET_REQ()}\n"
                f"CAREER:     {i.GET_CAR()}\n"
                f"JOB:        {i.GET_JOB()}\n"
                f"TUITION:    {i.GET_TUT()}\n"
                f"LOAN:       {i.GET_LON()} (avg.)\n"
                f"REPAY IN:   {i.GET_MTH_PAY()} months (est.)\n"
            )
            report += "─" * 32 + "\n"
        return report

    def export_data(self):
        path = os.path.join(os.path.normpath(os.path.expanduser("~/Desktop")), "output")
        if not os.path.exists(path):
            os.makedirs(path)

        str_time = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
        os.makedirs(os.path.join(path, str_time))

        f_name_ctree = f"Tree_{str_time}.txt"
        path_ctree = os.path.join(os.path.join(path, str_time), f_name_ctree)
        with open(path_ctree, 'w', encoding="utf-8") as f:
            f.write(f"{'─' * 32}\n{self.career_tree.STR()}\n{'─' * 32}")

        if self.college_info:
            f_name_colrep = f"Report_{str_time}.txt"
            path_colrep = os.path.join(os.path.join(path, str_time), f_name_colrep)
            with open(path_colrep, 'w', encoding="utf-8") as f:
                f.write(self.get_college_report())

        self.print_message(f"Exported Career Tree & College Report to {path}")

    def set_style_light(self):
        style = """
            QWidget {
                background-color: #F3F3F3;
                color: #000000;
                font-family: 'Consolas';
                font-size: 14px;
            }
            QLineEdit {
                background-color: #FFFFFF;
                border: 1px solid #CCCCCC;
                padding: 8px;
                border-radius: 5px;
                color: #000000;
            }
            QLineEdit:focus {
                border: 1px solid #2FB7E0;
            }
            QTextEdit {
                background-color: #FFFFFF;
                border: 1px solid #CCCCCC;
                padding: 8px;
                border-radius: 5px;
                color: #000000;
            }
            QPushButton {
                background-color: #2FB7E0;
                border: 2px solid #279ABA;
                color: #000000;
                padding: 4px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #279ABA;
            }
            QPushButton:pressed {
                background-color: #279ABA;
            }
            QPushButton:disabled {
                background-color: #BBBBBB;
                color: #000000;
                border: 2px solid #999999;
            }
        """
        self.setStyleSheet(style)
    
    def set_style_dark(self):
        style = """
            QWidget {
                background-color: #2E2E2E;
                color: #F0F0F0;
                font-family: 'Consolas';
                font-size: 14px;
            }
            QLineEdit {
                background-color: #3E3E3E;
                border: 1px solid #666666;
                padding: 8px;
                border-radius: 5px;
                color: #F0F0F0;
            }
            QLineEdit:focus {
                border: 1px solid #4DDDA6;
            }
            QTextEdit {
                background-color: #3E3E3E;
                border: 1px solid #666666;
                padding: 8px;
                border-radius: 5px;
                color: #F0F0F0;
            }
            QPushButton {
                background-color: #4DDDA6;
                border: 2px solid #43BA8A;
                color: #FFFFFF;
                padding: 2px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #43BA8A;
            }
            QPushButton:pressed {
                background-color: #43BA8A;
            }
            QPushButton:disabled {
                background-color: #BBBBBB;
                color: #FFFFFF;
                border: 2px solid #999999;
            }
        """
        self.setStyleSheet(style)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CareerTreeGUI()
    window.show()
    sys.exit(app.exec())