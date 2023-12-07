from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
import sys
import pymysql as mysql

conn = mysql.connect(
    host="127.0.0.1",
    port=3306,
    user="cs5330",
    password="cs5330",
    database="dbprog"
)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Database Project")
        self.setGeometry(100, 100, 600, 400)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.init_ui()
        self.setupDatabaseConnection()

    def init_ui(self):
        # Create the pages and add them to the stacked widget
        self.query_page = QueryPage(self)
        self.data_entry_page = DataEntryPage(self)

        self.stacked_widget.addWidget(self.query_page)
        self.stacked_widget.addWidget(self.data_entry_page)

    def setupDatabaseConnection(self):
        self.conn = None  # Database connection
        # Establish a connection to your database here
        self.conn = mysql.connect(
            host="127.0.0.1",
            port=3306,
            user="cs5330",
            password="cs5330",
            database="dbprog"
        )

    def navigate_to_query_page(self):
        self.stacked_widget.setCurrentWidget(self.query_page)

    def navigate_to_data_entry_page(self):
        self.stacked_widget.setCurrentWidget(self.data_entry_page)

class QueryPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.data_entry_layout = None

        # Query input field
        self.query_input_layout = QHBoxLayout()
        self.query_input_layout.addWidget(QLabel("Search by:"))
        self.query_dropdown = QComboBox(self)
        self.query_dropdown.addItems(["Department", "Program", "Semester + Program", "Academic Year"])
        self.query_dropdown.currentIndexChanged.connect(self.updateContent)
        self.query_input_layout.addWidget(self.query_dropdown)
        self.layout.addWidget(QLabel("Enter Query Parameters:"))
        self.layout.addLayout(self.query_input_layout)
        self.updateContent(self.query_dropdown.currentIndex())
        # Execute query button
        self.query_button = QPushButton("Execute Query", self)
        self.query_button.clicked.connect(self.executeQuery)
        self.layout.addWidget(self.query_button)

        # Results display area
        self.results_display = QTextEdit(self)
        self.results_display.setReadOnly(True)
        self.layout.addWidget(QLabel("Results:"))
        self.layout.addWidget(self.results_display)

        # Page navigation button
        self.other_page_button = QPushButton("Go to Data Entry Page")
        self.other_page_button.clicked.connect(parent.navigate_to_data_entry_page)
        self.layout.addWidget(self.other_page_button)

        self.setLayout(self.layout)

    def executeQuery(self):
        # Extract query parameters from input field

        if self.query_dropdown.currentIndex() == 0:
            query_param = self.input1.text()
            print(query_param)
            query = self.departmentQuery(query_param)
            results = [result for result in query]
            # concatinate results into a string
            results = '\n'.join([str(result) for result in results])
            self.results_display.setText(results)
        elif self.query_dropdown.currentIndex() == 1:
            query_param = self.input1.text()
            print(query_param)
            query = self.programQuery(query_param)
            results = [result for result in query]
            # concatinate results into a string
            results = '\n'.join([str(result) for result in results])
            self.results_display.setText(results)
        elif self.query_dropdown.currentIndex() == 2:
            program = self.input1.text()
            semester= self.input2.text()[:-4]
            # get year from semester
            year = semester[-4:]
            query = self.semesterAndProgramQuery(program, semester, year)
            results = [result for result in query]
            # concatinate results into a string
            results = '\n'.join([str(result) for result in results])
            self.results_display.setText(results)



    def departmentQuery(self, input):
        print(input)
        query = f"""SELECT 
                        D.DepartmentName, 
                        P.ProgramName, 
                        F.FacultyName, 
                        F.FacultyRank
                    FROM 
                        Department D
                    LEFT JOIN 
                        Program P ON D.DepartmentCode = P.DepartmentCode
                    LEFT JOIN 
                        Faculty F ON D.DepartmentCode = F.DepartmentCode
                    WHERE 
                        D.DepartmentCode = \'{input}\';
                    """
        cursor=conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results

    def programQuery(self, input):
        print(input)
        query = f"""
        SELECT 
            LO.ObjectiveCode,
            LO.ObjectiveDescription
        FROM 
            Program P
        JOIN 
            LearningObjective LO ON P.ProgramName = LO.ProgramName
        WHERE 
            P.ProgramName = \'{input}\';
        """
        cursor=conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results

    def semesterAndProgramQuery(self, input1, input2, input3):
        query = f"""
        SELECT 
         S.Semester, 
        S.Year, 
        S.SectionNumber, 
        C.CourseTitle, 
        F.FacultyName, 
        SO.ObjectiveCode, 
        SO.EvaluationMethod, 
        COALESCE(SO.NumberOfStudentsMet, 'Information Not Found') as EvaluationResult
        FROM 
            Program P
        JOIN ProgramCourse PC ON P.ProgramName = PC.ProgramName
        JOIN Course C ON PC.CourseID = C.CourseID
        JOIN Section S ON C.CourseID = S.CourseID
        JOIN Faculty F ON S.FacultyID = F.FacultyID
        LEFT JOIN SectionObjective SO ON S.SectionNumber = SO.SectionNumber 
        AND S.Semester = SO.Semester 
        AND S.Year = SO.Year
        WHERE 
            P.ProgramName = \'{input1}\' AND 
            S.Semester = \'{input2}\' AND 
            S.Year = \'{input3}\'
        ORDER BY 
        S.SectionNumber, SO.ObjectiveCode;
        """
        cursor=conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results



    def updateContent(self, index):
        # Clear existing content
        if self.data_entry_layout:
            for i in reversed(range(self.data_entry_layout.count())):
                widget_to_remove = self.data_entry_layout.itemAt(i).widget()
                self.data_entry_layout.removeWidget(widget_to_remove)
                widget_to_remove.setParent(None)
        self.input1 = None
        self.input2 = None
        # Add new content based on the selected option
        # 2 input fields for Semester + Program
        if index == 2:
            self.data_entry_layout = QHBoxLayout()
            self.input1 = QLineEdit(self)
            self.data_entry_layout.addWidget(self.input1)
            self.input2 = QLineEdit(self)
            self.data_entry_layout.addWidget(self.input2)
            self.query_input_layout.addLayout(self.data_entry_layout)
        else:  # One input for everything else
            self.data_entry_layout = QHBoxLayout()
            self.input1 = QLineEdit(self)
            self.data_entry_layout.addWidget(self.input1)
            self.query_input_layout.addLayout(self.data_entry_layout)

class DataEntryPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.subobjective_layouts =[]
        # Initialize data entry area
        self.data_dropdown_layout = QHBoxLayout()
        self.data_dropdown_layout.addWidget(QLabel("Entering:"))
        self.options_dropdown = QComboBox(self)
        self.options_dropdown.addItems(["Department", "Faculty", "Programs", "Courses", "Sections", "Objectives"])
        self.options_dropdown.currentIndexChanged.connect(self.updateContent)
        self.data_dropdown_layout.addWidget(self.options_dropdown)
        self.layout.addLayout(self.data_dropdown_layout)


        # Initialize content area
        self.content_area = QWidget(self)
        self.content_layout = QVBoxLayout(self.content_area)
        self.layout.addWidget(self.content_area)
        self.updateContent(self.options_dropdown.currentIndex())
        self.entry_success = QLabel("Entry Successful!")
        self.layout.addWidget(self.entry_success)
        # Execute data entry button
        submit_button = QPushButton("Submit Data")
        submit_button.clicked.connect(self.enterData)
        self.layout.addWidget(submit_button)

        # Navigation to other page
        button = QPushButton("Go to Query Page")
        button.clicked.connect(parent.navigate_to_query_page)
        self.layout.addWidget(button)

        self.setLayout(self.layout)

    def updateContent(self, index):
        # Clear existing content
        self.input1 = None
        self.input2 = None
        self.input3 = None
        self.input4 = None
        self.input5 = None
        self.subobjectives = []
        self.subobjective_desc = []
        clearLayout(self.content_layout)
        # Add new content based on the selected option
        # Entering Department
        if index == 0:
            self.data_entry_layout = QHBoxLayout()
            self.data_entry_layout.addWidget(QLabel("Dept. Name:"))
            self.input1 = QLineEdit(self)
            self.data_entry_layout.addWidget(self.input1)
            self.data_entry_layout.addWidget(QLabel("Dept. Code:"))
            self.input2 = QLineEdit(self)
            self.data_entry_layout.addWidget(self.input2)
            self.content_layout.addLayout(self.data_entry_layout)
        # Entering Faculty
        elif index == 1:
            self.data_entry_layout = QHBoxLayout()
            self.data_entry_layout.addWidget(QLabel("Name:"))
            self.input1 = QLineEdit(self)
            self.data_entry_layout.addWidget(self.input1)
            self.data_entry_layout.addWidget(QLabel("ID:"))
            self.input2 = QLineEdit(self)
            self.data_entry_layout.addWidget(self.input2)
            self.data_entry_layout.addWidget(QLabel("Dept.:"))
            self.input3 = QLineEdit(self)
            self.data_entry_layout.addWidget(self.input3)
            self.data_entry_layout2 = QHBoxLayout()
            self.data_entry_layout2.addWidget(QLabel("E-mail:"))
            self.input4 = QLineEdit(self)
            self.data_entry_layout2.addWidget(self.input4)
            self.data_entry_layout2.addWidget(QLabel("Rank:"))
            self.input5 = QLineEdit(self)
            self.data_entry_layout2.addWidget(self.input5)
            self.content_layout.addLayout(self.data_entry_layout)
            self.content_layout.addLayout(self.data_entry_layout2)
        # Entering Programs
        if index == 2:
            self.data_entry_layout = QHBoxLayout()
            self.data_entry_layout.addWidget(QLabel("Program Name:"))
            self.input1 = QLineEdit(self)
            self.data_entry_layout.addWidget(self.input1)
            self.data_entry_layout.addWidget(QLabel("Dept.:"))
            self.input2 = QLineEdit(self)
            self.data_entry_layout.addWidget(self.input2)
            self.data_entry_layout.addWidget(QLabel("Program Head ID:"))
            self.input3 = QLineEdit(self)
            self.data_entry_layout.addWidget(self.input3)
            self.content_layout.addLayout(self.data_entry_layout)
        # Entering Courses
        if index == 3:
            self.data_entry_layout = QHBoxLayout()
            self.data_entry_layout.addWidget(QLabel("Course Name:"))
            self.input1 = QLineEdit(self)
            self.data_entry_layout.addWidget(self.input1)
            self.data_entry_layout.addWidget(QLabel("Course Code:"))
            self.input2 = QLineEdit(self)
            self.data_entry_layout.addWidget(self.input2)
            self.data_entry_layout2 = QHBoxLayout()
            self.data_entry_layout2.addWidget(QLabel("Course Description:"))
            self.input3 = QLineEdit(self)
            self.data_entry_layout2.addWidget(self.input3)
            self.content_layout.addLayout(self.data_entry_layout)
            self.content_layout.addLayout(self.data_entry_layout2)
        # Entering Sections
        if index == 4:
            self.data_entry_layout = QHBoxLayout()
            self.data_entry_layout.addWidget(QLabel("Course Code:"))
            self.input1 = QLineEdit(self)
            self.data_entry_layout.addWidget(self.input1)
            self.data_entry_layout.addWidget(QLabel("Section Code:"))
            self.input2 = QLineEdit(self)
            self.data_entry_layout.addWidget(self.input2)
            self.data_entry_layout.addWidget(QLabel("No. Students:"))
            self.input3 = QLineEdit(self)
            self.data_entry_layout.addWidget(self.input3)
            self.data_entry_layout2 = QHBoxLayout()
            self.data_entry_layout2.addWidget(QLabel("Section Semester:"))
            self.input4 = QLineEdit(self)
            self.data_entry_layout2.addWidget(self.input4)
            self.data_entry_layout2.addWidget(QLabel("Section Year:"))
            self.input5 = QLineEdit(self)
            self.data_entry_layout2.addWidget(self.input5)
            self.data_entry_layout2.addWidget(QLabel("Section Faculty:"))
            self.input6 = QLineEdit(self)
            self.data_entry_layout2.addWidget(self.input6)
            self.content_layout.addLayout(self.data_entry_layout)
            self.content_layout.addLayout(self.data_entry_layout2)
        if index == 5:
            self.data_entry_layout = QHBoxLayout()
            self.data_entry_layout.addWidget(QLabel("Objective Name:"))
            self.input1 = QLineEdit(self)
            self.data_entry_layout.addWidget(self.input1)
            self.data_entry_layout.addWidget(QLabel("Objective Description:"))
            self.input2 = QLineEdit(self)
            self.data_entry_layout.addWidget(self.input2)
            self.data_entry_layout.addWidget(QLabel("Program Name:"))
            self.input3 = QLineEdit(self)
            self.data_entry_layout.addWidget(self.input3)
            self.content_layout.addLayout(self.data_entry_layout)
            # create button to add subobjectives
            self.subobjective_button = QPushButton("Add Subobjective")
            self.subobjective_button.clicked.connect(self.addSubobjective)
            self.content_layout.addWidget(self.subobjective_button)
            # create button to remove subobjectives
            self.remove_subobjective_button = QPushButton("Remove Subobjective")
            self.remove_subobjective_button.clicked.connect(self.removeSubobjectives)
            self.content_layout.addWidget(self.remove_subobjective_button)

    def addSubobjective(self):
        # create new layout for subobjective
        self.subobjective_layouts.append(QHBoxLayout())
        # create new input fields for subobjective
        self.subobjective_layouts[-1].addWidget(QLabel("Subobjective Name:"))
        self.subobjectives.append(QLineEdit(self))
        self.subobjective_layouts[-1].addWidget(self.subobjectives[-1])
        self.subobjective_layouts[-1].addWidget(QLabel("Subobjective Description:"))
        self.subobjective_desc.append(QLineEdit(self))
        self.subobjective_layouts[-1].addWidget(self.subobjective_desc[-1])
        # add subobjective layout to content layout
        self.content_layout.addLayout(self.subobjective_layouts[-1])

    def removeSubobjectives(self):
        # remove last subobjective
        clearLayout(self.subobjective_layouts[-1])
        self.subobjective_layouts[-1].setParent(None)
        self.subobjective_layouts.pop()

    def enterDepartment(self, input1, input2):
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Department VALUES (%s, %s);", (input1, input2))
            conn.commit()
            self.entry_success.setText("Entry Successful!")
        except:
            self.entry_success.setText("Entry Failed!")

    def enterFaculty(self, name, id, dept, email, rank):
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Faculty VALUES (%s, %s, %s, %s, %s);", (id, name, email, rank, dept))
            conn.commit()
            self.entry_success.setText("Entry Successful!")
        except:
            self.entry_success.setText("Entry Failed!")


    def enterProgram(self, name, dept, id):
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Program VALUES (%s, %s, %s);", (name, id, dept))
            conn.commit()
            self.entry_success.setText("Entry Successful!")
        except:
            self.entry_success.setText("Entry Failed!")


    def enterCourse(self, name, code, desc):
        # get the department code by stripping the last 4 characters from the course code
        dept = code[:-4]
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Course VALUES (%s, %s, %s, %s);", (code, name, desc, dept))
            conn.commit()
            self.entry_success.setText("Entry Successful!")
        except:
            self.entry_success.setText("Entry Failed!")

    def enterSection(self, course, section, students, semester, year, faculty):
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Section VALUES (%s, %s, %s, %s, %s, %s);", (section, semester, year, course, faculty, students))
            conn.commit()
            self.entry_success.setText("Entry Successful!")
        except:
            self.entry_success.setText("Entry Failed!")

    def enterObjective(self, name, desc, program):
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO LearningObjective VALUES (%s, %s, %s);", (name, desc, program))
            conn.commit()
            self.entry_success.setText("Entry Successful!")
        except:
            self.entry_success.setText("Entry Failed!")
            return
        for i in range(len(self.subobjectives)):
            sub_name = name + "." + (i+1).__str__()
            try:
                cursor.execute("INSERT INTO SubObjective VALUES (%s, %s, %s);", (sub_name, self.subobjectives[i].text(), name))
                conn.commit()
                self.entry_success.setText("Entry Successful!")
            except:
                self.entry_success.setText("Entry Failed!")
                return

    def enterData(self):
        # For entering Department
        if self.options_dropdown.currentIndex() == 0:
            self.enterDepartment(self.input1.text(), self.input2.text())

        # For entering Faculty
        elif self.options_dropdown.currentIndex() == 1:
            self.enterFaculty(self.input1.text(), self.input2.text(), self.input3.text(), self.input4.text(), self.input5.text())

        # For entering Programs
        elif self.options_dropdown.currentIndex() == 2:
            self.enterProgram(self.input1.text(), self.input2.text(), self.input3.text())

        # For entering Courses
        elif self.options_dropdown.currentIndex() == 3:
            self.enterCourse(self.input1.text(), self.input2.text(), self.input3.text())

        # For entering Sections
        elif self.options_dropdown.currentIndex() == 4:
            self.enterSection(self.input1.text(), self.input2.text(), self.input3.text(), self.input4.text(), self.input5.text(), self.input6.text())

        # For entering Objectives
        elif self.options_dropdown.currentIndex() == 5:
            self.enterObjective(self.input1.text(), self.input2.text(), self.input3.text())

        # Perform database query using self.db_connection
        # For example:
        # cursor = self.db_connection.cursor()
        # cursor.execute("SELECT * FROM your_table WHERE condition = ?", (query_param,))
        # results = cursor.fetchall()
        # Display results in the results_display widget
        # This is a placeholder for actual database query handling
        #self.results_display.setText("Results for query: " + query_param)

def clearLayout(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()
        else:
            # If the item is a layout, this will recursively clear any child layouts
            child_layout = item.layout()
            if child_layout is not None:
                clearLayout(child_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

#%%
