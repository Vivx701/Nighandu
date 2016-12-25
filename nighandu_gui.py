import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton
from PyQt5.QtWidgets import QSizePolicy, QScrollArea
from PyQt5.QtCore import Qt,  pyqtSlot
from nighandu import Nighandu


class NighanduGui(QWidget):

    def __init__(self, parent=None):
        super(NighanduGui, self).__init__(parent)

        self.nighandu = Nighandu("olam-enml.csv")
        self.initUI()

    def initUI(self):

        
        #widget properties 
        self.setMinimumSize(340, 420)



        mainLayout = QVBoxLayout()
       

        #inputs Widgets
        inputLayout = QHBoxLayout()
        self.searchButton = QPushButton("&Search", self)
        self.searchButton.setFixedSize(80, 30)
        self.searchButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.searchButton.clicked.connect(self.searchButtonClicked)


        self.wordInput = QLineEdit(self)
        self.wordInput.setFixedHeight(30)
        self.wordInput.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.wordInput.returnPressed.connect(self.searchButtonClicked)

        inputLayout.addWidget(self.wordInput)
        inputLayout.addWidget(self.searchButton)
        mainLayout.addLayout(inputLayout)


        self.wordViewerLabel = QLabel(self)
        self.wordViewerScrollArea = QScrollArea(self)
        self.wordViewerScrollArea.setWidgetResizable(True)
        self.wordViewerScrollArea.setWidget(self.wordViewerLabel)
        self.wordViewerScrollArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        mainLayout.addWidget(self.wordViewerScrollArea)


 
        self.setLayout(mainLayout)


    @pyqtSlot()
    def searchButtonClicked(self):
        results = self.searchMeaning(self.wordInput.text())
        if results == None:
            txt ="Sorry No results Found"
        else:
            txt = ""
            for result in results:
                txt = txt+(result['malayalam_definition']+"\n")
        self.wordViewerLabel.setText(txt)




    def searchMeaning(self, word):
        results = self.nighandu.search_word(word)
        return results

        

        
        










if __name__ == "__main__":

    app = QApplication(sys.argv)
    nighanduGui = NighanduGui()
    nighanduGui.show()
    sys.exit(app.exec_())  