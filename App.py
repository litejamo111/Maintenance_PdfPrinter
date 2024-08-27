from PyQt6.QtWidgets import QPushButton, QLineEdit, QApplication, QFormLayout, QWidget, QTextEdit, QMessageBox, QSpinBox, QComboBox
from PyQt6.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal, pyqtSlot

from reportlab.pdfgen.canvas import Canvas

import os

import textwrap
from datetime import datetime

from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl

OUTPUT_PATH = r"youroutputpath"

class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.
    """
    error = pyqtSignal(str)
    file_saved_as = pyqtSignal(str)


class Generator(QRunnable):
    def __init__(self, data, num_equipo, template_file="template_Gblab.pdf"):
        super().__init__()
        self.data = data
        self.num_equipo = num_equipo
        self.template_file = template_file
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            outfile = os.path.join(OUTPUT_PATH, f"{self.num_equipo}.pdf")

            # Ensure the directory exists
            os.makedirs(os.path.dirname(outfile), exist_ok=True)
            
            template = PdfReader(self.template_file, decompress=False).pages[0]
            template_obj = pagexobj(template)

            canvas = Canvas(outfile)

            xobj_name = makerl(canvas, template_obj)
            canvas.doForm(xobj_name)

            # Adjust these Y-coordinates based on the actual layout of your PDF
            ystart = 503  # You'll need to adjust this value

            # Realizado Por
            canvas.drawString(145, ystart, self.data['name'])

            # Fecha
            today = datetime.today()
            canvas.drawString(407, ystart, today.strftime('%d/%m/%Y'))
            # # Equipo
            canvas.drawString(112, ystart-37, self.data['num_equipo'])

            # Usuario
            canvas.drawString(265, ystart-37, self.data['usuario'])
            
            # Marca
            canvas.drawString(95, ystart-73, self.data['marca'])

            # Modelo
            canvas.drawString(260, ystart-73, self.data['modelo'])

            # Procesador
            canvas.drawString(130, ystart-106, self.data['procesador'])

            # Tarjeta Grafica
            canvas.drawString(380, ystart-106, self.data['tarjeta_grafica'])
            
            # Ram
            canvas.drawString(80, ystart-142, self.data['ram'])

            # Almacenamiento
            canvas.drawString(315, ystart-142, self.data['almacenamiento'])

            # Presento Novedades
            canvas.drawString(195, ystart-256, self.data['novedades'])

            # G. de las Novedades
            canvas.drawString(432, ystart-256, self.data['gravedad_novedades'])

            # Observaciones
            comments = self.data['observaciones'].replace('\n', ' ')
            if comments:
                # Wrap the entire text
                all_lines = textwrap.wrap(comments, width=65)
                
                # First line
                if all_lines:
                    first_line = all_lines[0]
                    canvas.drawString(136, ystart-285, first_line)
                
                # Remaining lines
                if len(all_lines) > 1:
                    remainder = ' '.join(all_lines[1:])
                    remaining_lines = textwrap.wrap(remainder, width=90)
                    remaining_lines = remaining_lines[:4]  # max 4 additional lines
                    
                    for n, line in enumerate(remaining_lines, 1):
                        canvas.drawString(40, ystart-285-(n*30), line)
                        
            canvas.save()

        except Exception as e:
            self.signals.error.emit(str(e))
            return

        self.signals.file_saved_as.emit(outfile)


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.threadpool = QThreadPool()

        self.name = QComboBox()
        self.name.addItems(['Jose David Lopez Jaramillo','Santiago Quiceno Gomez'])
        self.num_equipo = QLineEdit()
        self.usuario = QLineEdit()
        self.marca = QComboBox()
        self.marca.addItems(['Dell','Asus','Hp','Acer','Lenovo','Msi','Gigabyte'])
        self.modelo = QLineEdit()
        self.procesador = QLineEdit()
        self.tarjeta_grafica = QLineEdit()
        self.ram = QLineEdit()
        self.almacenamiento = QLineEdit()
        self.novedades = QComboBox()
        self.novedades.addItems(['No','Si'])
        self.gravedad_novedades = QComboBox()
        self.gravedad_novedades.addItems(['No Aplica','Bajo','Medio','Alto'])
        self.observaciones = QTextEdit()

        self.generate_btn = QPushButton("Generate PDF")
        self.generate_btn.pressed.connect(self.generate)

        layout = QFormLayout()
        layout.addRow("Realizado Por", self.name)
        layout.addRow("# Equipo", self.num_equipo)
        layout.addRow("Usuario", self.usuario)
        layout.addRow("Marca", self.marca)
        layout.addRow("Modelo", self.modelo)
        layout.addRow("Procesador", self.procesador)
        layout.addRow("Tarjeta Grafica", self.tarjeta_grafica)
        layout.addRow("Ram", self.ram)
        layout.addRow("Almacenamiento", self.almacenamiento)
        layout.addRow("Presento Novedades", self.novedades)
        layout.addRow("G. de las Novedades", self.gravedad_novedades)
        layout.addRow("Observaciones", self.observaciones)
        layout.addRow(self.generate_btn)

        self.setLayout(layout)

    def generate(self):
        self.generate_btn.setDisabled(True)
        data = {
            'name': self.name.currentText(),  # Changed from text() to currentText()
            'num_equipo': self.num_equipo.text(),
            'usuario': self.usuario.text(),
            'marca': self.marca.currentText(),  # Changed from text() to currentText()
            'modelo': self.modelo.text(),
            'procesador': self.procesador.text(),
            'tarjeta_grafica': self.tarjeta_grafica.text(),
            'ram': self.ram.text(),
            'almacenamiento': self.almacenamiento.text(),
            'novedades': self.novedades.currentText(),  # Changed from text() to currentText()
            'gravedad_novedades': self.gravedad_novedades.currentText(),  # Changed from text() to currentText()
            'observaciones': self.observaciones.toPlainText()
        }
        num_equipo = self.num_equipo.text()
        g = Generator(data, num_equipo)
        g.signals.file_saved_as.connect(self.generated)
        g.signals.error.connect(print)  # Print errors to console.
        self.threadpool.start(g)

    def generated(self, outfile):
        self.generate_btn.setDisabled(False)
        try:
            os.startfile(outfile)
        except Exception:
            # If startfile not available, show dialog with the file path
            QMessageBox.information(self, "Finished", f"PDF has been generated and saved to:\n{outfile}")

app = QApplication([])
w = Window()
w.show()
app.exec()