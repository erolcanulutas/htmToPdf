import os
import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QTimer

class HTMLtoPDFConverter(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        self.import_button = QPushButton("Import")
        self.import_button.clicked.connect(self.import_file)
        button_layout.addWidget(self.import_button)

        self.export_button = QPushButton("Export as PDF")
        self.export_button.clicked.connect(self.export_pdf)
        button_layout.addWidget(self.export_button)

        main_layout.addLayout(button_layout)

        self.info_label = QLabel("No file imported")
        main_layout.addWidget(self.info_label)

        self.web_view = QWebEngineView()
        
        self.setLayout(main_layout)

        # Variable to remember the last directory accessed
        self.last_directory = ""

    def import_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Import File", self.last_directory, "HTML Files (*.html *.htm *.mhtml *.mht)", options=options)
        
        if file_path:
            self.last_directory = os.path.dirname(file_path)
            self.info_label.setText(f"Name: {os.path.basename(file_path)}\nLocation: {os.path.dirname(file_path)}\nExtension: {os.path.splitext(file_path)[1]}\nSize: {os.path.getsize(file_path)} bytes")
            self.web_view.setUrl(QUrl.fromLocalFile(file_path))
            self.imported_file_path = file_path

    def export_pdf(self):
        if hasattr(self, 'imported_file_path'):
            options = QFileDialog.Options()
            save_path, _ = QFileDialog.getSaveFileName(self, "Save File", self.last_directory, "PDF Files (*.pdf)", options=options)

            if save_path:
                if not save_path.endswith('.pdf'):
                    save_path += '.pdf'
                
                self.last_directory = os.path.dirname(save_path)
                
                def save():
                    self.web_view.page().printToPdf(save_path)
                    # Open the folder containing the saved file and select the file
                    subprocess.Popen(f'explorer /select,"{os.path.abspath(save_path)}"')
                
                QTimer.singleShot(2000, save)

app = QApplication(sys.argv)
window = HTMLtoPDFConverter()
window.show()
app.exec_()
