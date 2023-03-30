from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QLabel, QPushButton, QGridLayout, QLineEdit,  QSizePolicy, QLayout
from PySide6.QtCore import SIGNAL, SLOT, Qt
from PySide6.QtGui import QPixmap

import sys
import logging
import cv2
import tensorflow as tf

IMAGE_SIZE = 400


class MainWindow(QMainWindow):
    # Constructor function
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initGUI()
    
    def initGUI(self):
        logging.debug('Running main window')
        self.setWindowTitle("Demonstrating trained model")

        # Set up size
        self.setMinimumHeight(700)
        self.setMinimumWidth(500)

        # Set up layout
        self.setUpLayout()

        logging.debug('Showing main window')
        self.show()
          
    def setUpLayout(self):
        
        self.mainWidget = QWidget(self)
        self.setCentralWidget(self.mainWidget)
        self.mainLayout = QGridLayout(self.mainWidget)
        self.mainLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

        # Choose file
        logging.debug('Setting up invoice window')


        self.imageDisplay = QLabel(self)
        self.imageDisplay.setWordWrap(True)
        self.imageDisplay.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        self.mainLayout.addWidget(self.imageDisplay, 0, 0, 1, 3)

            
        self.getModelButton = QPushButton("Get model")
        self.mainLayout.addWidget(self.getModelButton, 1, 0)

        self.trainStatus = QLabel("No model has been chosen yet")
        self.mainLayout.addWidget(self.trainStatus, 1, 1, 1, 2)

        self.chooseFile = QPushButton("Choose image file", self)
        self.mainLayout.addWidget(self.chooseFile, 2, 0)

        self.addressText = QLineEdit(self)
        self.mainLayout.addWidget(self.addressText, 2, 1, 1, 2)


        self.identifyButton = QPushButton(self, text="Predict image")
        self.mainLayout.addWidget(self.identifyButton, 3, 0)

        self.resultText = QLabel("")
        self.mainLayout.addWidget(self.resultText, 4, 0)

        self.connect(self.chooseFile, SIGNAL("clicked()"), self, SLOT("getFileName()"))
        self.connect(self.getModelButton, SIGNAL("clicked()"), self, SLOT("getModel()"))
        self.connect(self.identifyButton, SIGNAL("clicked()"), self, SLOT("identifyImage()"))
  

        self.setLayout(self.mainLayout)

    def getModel(self):
        self.folderDialog = QFileDialog()
        self.folderName = self.folderDialog.getExistingDirectory()

        self.model = tf.keras.models.load_model(self.folderName)
        if not self.model:
            return False
        
        model_name = self.folderName.split("traffic/")[1]
        self.trainStatus.setText(f"Model {model_name} successfully loaded")
    
    def getFileName(self):
        filename = QFileDialog.getOpenFileName()
        self.addressText.setText(filename[0])
        self.image = QPixmap(self.addressText.text())

        if not self.image:
            return False

        self.imageDisplay.setPixmap(self.image.scaled(IMAGE_SIZE, IMAGE_SIZE, Qt.IgnoreAspectRatio))


    def identifyImage(self):
        #if not self.model:
            #return False
        model_image_size = 30
        image_address = self.addressText.text()
        
        image_address = image_address.split("traffic/")[1]
        image_array = cv2.imread(image_address)
        new_image_array = cv2.resize(image_array, (model_image_size, model_image_size), interpolation = cv2.INTER_AREA)
        final_array = new_image_array.reshape(-1, model_image_size, model_image_size, 3)
        prediction = self.model.predict([final_array])
        result = prediction[0].tolist()
        result_signID = result.index(max(result))
        

        self.matching_image = QPixmap(f"Meta\{result_signID}.png")
        self.resultText.setPixmap(self.matching_image.scaled(100, 100, Qt.IgnoreAspectRatio))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    myApp = QApplication(sys.argv)
    myApp.setStyle("Fusion")

    myWindow = MainWindow()

    # Run the app
    sys.exit(myApp.exec())