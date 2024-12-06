import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtSql import QSqlDatabase, QSqlRelationalTableModel, QSqlQuery, QSqlRelation

class VariantsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Variants CRUD Application")
        self.setGeometry(100, 100, 800, 600)

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('variants.db')

        if not self.db.open():
            print("Error: Unable to connect to database")
            return

        self.create_tables()

        self.model = QSqlRelationalTableModel(self)
        self.model.setTable('Variants')
        self.model.setEditStrategy(QSqlRelationalTableModel.OnFieldChange)
        
        self.model.setRelation(2, QSqlRelation('Categories', 'id', 'name'))
        self.model.select()

        self.table_view = QTableView(self)
        self.table_view.setModel(self.model)

        self.add_button = QPushButton("Add Variant", self)
        self.add_button.clicked.connect(self.add_variant)

        self.update_button = QPushButton("Update Variant", self)
        self.update_button.clicked.connect(self.update_variant)

        self.delete_button = QPushButton("Delete Variant", self)
        self.delete_button.clicked.connect(self.delete_variant)

        layout = QVBoxLayout()
        layout.addWidget(self.table_view)
        layout.addWidget(self.add_button)
        layout.addWidget(self.update_button)
        layout.addWidget(self.delete_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def create_tables(self):
        query = QSqlQuery()

        query.exec_('''CREATE TABLE IF NOT EXISTS Variants (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        category_id INTEGER,
                        price REAL,
                        FOREIGN KEY(category_id) REFERENCES Categories(id))''')

        query.exec_('''CREATE TABLE IF NOT EXISTS Categories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL)''')

        query.exec_("INSERT OR IGNORE INTO Categories (name) VALUES ('Category 1')")
        query.exec_("INSERT OR IGNORE INTO Categories (name) VALUES ('Category 2')")

    def add_variant(self):
        name = "New Variant"
        category_id = 1
        price = 100.0
        query = QSqlQuery()
        query.prepare("INSERT INTO Variants (name, category_id, price) VALUES (?, ?, ?)")
        query.addBindValue(name)
        query.addBindValue(category_id)
        query.addBindValue(price)
        query.exec_()

        self.model.select()

    def update_variant(self):
        index = self.table_view.selectedIndexes()
        if index:
            row = index[0].row()
            self.model.setData(self.model.index(row, 1), "Updated Variant Name")
            self.model.setData(self.model.index(row, 2), 2)
            self.model.setData(self.model.index(row, 3), 200.0)
            self.model.submitAll()

    def delete_variant(self):
        index = self.table_view.selectedIndexes()
        if index:
            row = index[0].row()
            self.model.removeRow(row)
            self.model.submitAll()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VariantsApp()
    window.show()
    sys.exit(app.exec_())
