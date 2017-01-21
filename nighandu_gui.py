import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton
from PyQt5.QtWidgets import QSizePolicy, QScrollArea
from PyQt5.QtCore import Qt,  pyqtSlot
from nighandu import Nighandu


class NighanduGui(QWidget):

    def __init__(self, parent=None):
        super(NighanduGui, self).__init__(parent)

        self.nighandu = Nighandu("olam-enml.csv")
        self.window().setWindowTitle("Nighandu")
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

        #change case
        word = self.wordInput.text().lower()
        word = word.replace(word[0], word[0].upper(), 1)
 

        results = self.searchMeaning(word)

        if results == None:
            txt ="Sorry No results Found"
        else:
           
           txt = self.formatResults(results)
        self.wordViewerLabel.setText(txt)



    def formatResults(self, results):

        verbs = []
        nouns = []
        adjectives = []
        adverbs = []
        pronouns = []
        properNouns = []
        phrasalVerbs = []
        conjunctions = []
        interjections = []
        prepositions = []
        prefixs = []
        suffixs = []
        idioms = []
        abbreviations = []
        auxiliaryVerbs = []



        for result in results:

            if result['part_of_speech'] == "n":
                nouns.append(result['malayalam_definition'])
            elif result['part_of_speech'] == "v":
                verbs.append(result['malayalam_definition'])
            elif result['part_of_speech'] == "a":
                adjectives.append(result['malayalam_definition'])
            elif result['part_of_speech'] == "adv":
                adverbs.append(result['malayalam_definition'])

            elif result['part_of_speech'] == "pron":
                pronouns.append(result['malayalam_definition'])
            elif result['part_of_speech'] == "propn":
                properNouns.append(result['malayalam_definition'])
            elif result['part_of_speech'] == "phrv":
                phrasalVerbs.append(result['malayalam_definition'])
            elif result['part_of_speech'] == "conj":
                conjunctions.append(result['malayalam_definition'])
            elif result['part_of_speech'] == "interj":
                interjections.append(result['malayalam_definition'])
            elif result['part_of_speech'] == "prep":
                prepositions.append(result['malayalam_definition'])
            elif result['part_of_speech'] == "pfx":
                prefixs.append(result['malayalam_definition'])

            elif result['part_of_speech'] == "sfx":
                suffixs.append(result['malayalam_definition'])

            elif result['part_of_speech'] == "abbr":
                abbreviations.append(result['malayalam_definition'])

            elif result['part_of_speech'] == "auxv":
                auxiliaryVerbs.append(result['malayalam_definition'])


            nounHtmlContent = "" if len(nouns) == 0 else  '''<hr/>
            <h3>നാമം <span>:Noun</span></h3>
            <hr/>'''


            for noun in nouns:
                nounHtmlContent += '''
                <li>{0}</li>
                '''.format(noun)
            


            verbHtmlContent = "" if len(verbs) == 0 else  '''
            <hr/>
            <h3>ക്രിയ <span> :Verb</span></h3>
            <hr/>
            '''
            for verb in verbs:
                verbHtmlContent += '''
                <li>{0}</li>
                '''.format(verb)


            adjectivesHtmlContent = "" if len(adjectives) == 0 else  '''<hr/>
            <h3>വിശേഷണം<span>:Adjective</span></h3>
            <hr/>'''
            for adjective in adjectives:
                adjectivesHtmlContent += '''
                <li>{0}</li>
                '''.format(adjective)
            


            adverbHtmlContent = "" if len(adverbs) == 0 else  '''
            <hr/>
            <h3>ക്രിയാവിശേഷണം<span> :Adverb</span></h3>
            <hr/>
            '''
            for adverb in adverbs:
                adverbHtmlContent += '''
                <li>{0}</li>
                '''.format(adverb)




            htmlContent = '''

            <h3>Word : {0} </h3>
            <ul>


            {1}


            {2}

            {3}


            {4}

            </ul>

            '''.format(self.wordInput.text().strip(), nounHtmlContent, verbHtmlContent, adjectivesHtmlContent, adverbHtmlContent)


        return htmlContent

    def searchMeaning(self, word):
        results = self.nighandu.search_word(word)
        return results

 

if __name__ == "__main__":

    app = QApplication(sys.argv)
    nighanduGui = NighanduGui()
    nighanduGui.show()
    sys.exit(app.exec_())  