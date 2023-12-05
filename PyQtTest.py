from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
import sys
import pymysql as mysql

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
        # self.conn = mysql.connect(
        #     host="127.0.0.1",
        #     port=3306,
        #     user="cs5330",
        #     password="cs5330",
        #     database="dbprog"
        # )

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
        # self.query_input = QLineEdit(self)
        # self.query_input_layout.addWidget(self.query_input)
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

        query_param = ""
        if self.input1:
            query_param = self.input1.text()
        if self.input2:
            query_param += " " + self.input2.text()
        # Perform database query using self.db_connection
        # For example:
        # cursor = self.db_connection.cursor()
        # cursor.execute("SELECT * FROM your_table WHERE condition = ?", (query_param,))
        # results = cursor.fetchall()
        # Display results in the results_display widget
        # This is a placeholder for actual database query handling
        self.results_display.setText("Results for query: " + query_param)

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
        if index == 2:  # Option 1
            self.data_entry_layout = QHBoxLayout()
            self.input1 = QLineEdit(self)
            self.data_entry_layout.addWidget(self.input1)
            self.input2 = QLineEdit(self)
            self.data_entry_layout.addWidget(self.input2)
            self.query_input_layout.addLayout(self.data_entry_layout)
        else:  # Option 2
            self.data_entry_layout = QHBoxLayout()
            self.input1 = QLineEdit(self)
            self.data_entry_layout.addWidget(self.input1)
            self.query_input_layout.addLayout(self.data_entry_layout)

class DataEntryPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.layout = QVBoxLayout()

        # Initialize data entry area
        self.data_dropdown_layout = QHBoxLayout()
        self.data_dropdown_layout.addWidget(QLabel("Entering:"))
        self.options_dropdown = QComboBox(self)
        self.options_dropdown.addItems(["Department", "Faculty", "Programs", "Courses", "Sections", "Sub-Objectives"])
        self.options_dropdown.currentIndexChanged.connect(self.updateContent)
        self.data_dropdown_layout.addWidget(self.options_dropdown)
        self.layout.addLayout(self.data_dropdown_layout)


        # Initialize content area
        self.content_area = QWidget(self)
        self.content_layout = QVBoxLayout(self.content_area)
        self.layout.addWidget(self.content_area)
        self.updateContent(self.options_dropdown.currentIndex())

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
            self.data_entry_layout2 = QHBoxLayout()
            self.data_entry_layout2.addWidget(QLabel("E-mail:"))
            self.input3 = QLineEdit(self)
            self.data_entry_layout2.addWidget(self.input3)
            self.data_entry_layout2.addWidget(QLabel("Rank:"))
            self.input4 = QLineEdit(self)
            self.data_entry_layout2.addWidget(self.input4)
            self.content_layout.addLayout(self.data_entry_layout)
            self.content_layout.addLayout(self.data_entry_layout2)
        # Entering Programs
        if index == 2:
            self.data_entry_layout = QHBoxLayout()
            self.data_entry_layout.addWidget(QLabel("Program Name:"))
            self.input1 = QLineEdit(self)
            self.data_entry_layout.addWidget(self.input1)
            self.data_entry_layout.addWidget(QLabel("Program Head:"))
            self.input2 = QLineEdit(self)
            self.data_entry_layout.addWidget(self.input2)
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
            self.data_entry_layout2 = QHBoxLayout()
            self.data_entry_layout2.addWidget(QLabel("Section Semester:"))
            self.input3 = QLineEdit(self)
            self.data_entry_layout2.addWidget(self.input3)
            self.data_entry_layout2.addWidget(QLabel("Section Year:"))
            self.input4 = QLineEdit(self)
            self.data_entry_layout2.addWidget(self.input4)
            self.data_entry_layout2.addWidget(QLabel("Section Faculty:"))
            self.input5 = QLineEdit(self)
            self.data_entry_layout2.addWidget(self.input5)
            self.content_layout.addLayout(self.data_entry_layout)
            self.content_layout.addLayout(self.data_entry_layout2)
    def enterData(self):
        # Extract query parameters from input field
        query_param = ""
        if self.input1:
            query_param = self.input1.text()
        if self.input2:
            query_param += " " + self.input2.text()
        if self.input3:
            query_param += " " + self.input3.text()
        if self.input4:
            query_param += " " + self.input4.text()
        if self.input5:
            query_param += " " + self.input5.text()
        print(query_param)
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
