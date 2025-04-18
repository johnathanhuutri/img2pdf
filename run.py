import sys
from PIL import Image
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox
from PySide6.QtCore import Qt, QFile

def showPopupInfo(title, msg):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)  # Options: Information, Warning, Critical, or Question
    msg_box.setWindowTitle(title)
    msg_box.setText(msg)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec()

def showPopupCritical(title, msg):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Critical)  # Options: Information, Warning, Critical, or Question
    msg_box.setWindowTitle(title)
    msg_box.setText(msg)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec()

def addImagePath():
    paths = QFileDialog.getOpenFileNames(None, "Open", "", "Images (*.png *.jpg *.jpeg)")[0]
    window.listWidget.addItems(paths)

def deleteImagePath():
    for item in window.listWidget.selectedItems():
        window.listWidget.takeItem(window.listWidget.row(item))

def convert():
    paths = [window.listWidget.item(i).text() for i in range(window.listWidget.count())]
    print(paths)

    if not paths:
        showPopupCritical('CONVERT', 'Please add an image first!')
        return

    output_path = QFileDialog.getSaveFileName(None, "Export to PDF", "", "PDF (*.pdf)")[0]
    if not output_path:
        return

    images = []
    for path in paths:
        img = Image.open(path).convert("RGB")
        images.append(img)
    try:
        images[0].save(output_path, save_all=True, append_images=images[1:])
        showPopupInfo('CONVERT', f'Created PDF at {output_path}')
    except Exception as e:
        showPopupCritical('CONVERT', str(e))

if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    ui_file = QFile("mainwindow.ui")
    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    window.show()                   # auto fork()


    window.btnAdd.clicked.connect(addImagePath)
    window.btnDelete.clicked.connect(deleteImagePath)
    window.btnConvert.clicked.connect(convert)

    sys.exit(app.exec())
