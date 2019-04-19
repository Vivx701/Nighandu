import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QListView
from PyQt5.QtWidgets import QSizePolicy, QScrollArea, QCompleter, QHBoxLayout,  QDialog
from PyQt5.QtCore import Qt,  pyqtSlot, QModelIndex
from PyQt5.QtCore import QStandardPaths
import requests, zipfile, io
from nighandu import Nighandu
import asyncio


OLAM_DATASET_URL = "https://olam.in/open/enml/olam-enml.csv.zip"
HOME_PATH = QStandardPaths.writableLocation(QStandardPaths.HomeLocation)
FILES_DIR = os.path.join(HOME_PATH, ".Nighandu")
class NighanduGui(QWidget):

    def __init__(self, parent=None):
        super(NighanduGui, self).__init__(parent)

        self.window().setWindowTitle("Nighandu")
        self.initApp()
        self.initUI()

    async def downloadOlamDataset(self, url, saveLocation):
        r = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(saveLocation)
      

    def initApp(self):
        
        if not os.path.exists(FILES_DIR):
            os.mkdir(FILES_DIR)
        
        csvFile = os.path.join(FILES_DIR, "olam-enml.csv")
        if not os.path.exists(csvFile):
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.downloadOlamDataset(OLAM_DATASET_URL, FILES_DIR))
        
        self.nighandu = Nighandu(csvFile)

    def initUI(self):

        #widget properties 
        self.setMinimumSize(895, 680)
        mainLayout = QHBoxLayout()
       
        #inputs Widgets
        inputLayout = QHBoxLayout()
        self.searchButton = QPushButton("&Search", self)
        self.searchButton.setFixedSize(80, 30)
        self.searchButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.searchButton.clicked.connect(self.searchButtonClicked)

        wordList = self.nighandu.word_list()
        self.wordInput = QLineEdit(self)
        self.wordInput.setFixedHeight(30)

        completer = QCompleter(wordList, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.wordInput.setCompleter(completer)

        self.wordInput.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.wordInput.returnPressed.connect(self.searchButtonClicked)

        inputLayout.addWidget(self.wordInput)
        inputLayout.addWidget(self.searchButton)

        leftControlsLayout = QVBoxLayout()
        leftControlsLayout.addLayout(inputLayout)

        suggesionsList = QListView(self)
        suggesionsList.setEditTriggers(QListView.NoEditTriggers)
        suggesionsList.setModel(completer.completionModel())
        suggesionsList.clicked.connect(self.suggesionsListClicked)
        leftControlsLayout.addWidget(suggesionsList)
        mainLayout.addLayout(leftControlsLayout)
        self.wordViewerLabel = QLabel(self)
        self.wordViewerScrollArea = QScrollArea(self)
        self.wordViewerScrollArea.setWidgetResizable(True)
        self.wordViewerScrollArea.setWidget(self.wordViewerLabel)
        self.wordViewerScrollArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.wordViewerLabel.setMargin(20)
        self.wordViewerLabel.setAlignment(Qt.AlignTop)
        #initial font size
        font = self.wordViewerLabel.font()
        font.setPixelSize(15)
        self.wordViewerLabel.setFont(font) 
        self.wordViewerLabel.setText("<center> <h1> Nighandu </h1></center>")       


        self.zoomInButton = QPushButton("ZoomIn (+)", self)
        self.zoomInButton.clicked.connect(self.zoomIn)
        self.zoomOutButton = QPushButton("ZoomOut (-)", self)
        self.zoomOutButton.clicked.connect(self.zoomOut)

        self.aboutButton = QPushButton("About", self)
        self.aboutButton.clicked.connect(self.about)


        zoomButtonLayout = QHBoxLayout()
        zoomButtonLayout.addWidget(self.aboutButton)
        zoomButtonLayout.addStretch()
        zoomButtonLayout.addWidget(self.zoomInButton)
        zoomButtonLayout.addWidget(self.zoomOutButton)
        
        rightConrolsLayout = QVBoxLayout()
        rightConrolsLayout.addWidget(self.wordViewerScrollArea)
        rightConrolsLayout.addLayout(zoomButtonLayout)

        mainLayout.addLayout(rightConrolsLayout)
 
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

    @pyqtSlot(QModelIndex)
    def suggesionsListClicked(self, index):

        results = self.searchMeaning(index.data())

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
        meanings = []



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

            elif result['part_of_speech'] == "idm":
                idioms.append(result['malayalam_definition'])
            else:
                meanings.append(result['malayalam_definition'])


            meaningHtmlContent = "" if len(meanings) == 0 else  '''<hr/>
            <h3>അര്‍ത്ഥം <span> :Meaning</span></h3>
            <hr/>'''


            for meaning in meanings:
                meaningHtmlContent += '''
                <li><h4>{0}</h4></li>
                '''.format(meaning)
            


            nounHtmlContent = "" if len(nouns) == 0 else  '''<hr/>
            <h3>നാമം <span>:Noun</span></h3>
            <hr/>'''


            for noun in nouns:
                nounHtmlContent += '''
                <li><h4>{0}</h4></li>
                '''.format(noun)
            


            verbHtmlContent = "" if len(verbs) == 0 else  '''
            <hr/>
            <h3>ക്രിയ <span> :Verb</span></h3>
            <hr/>
            '''
            for verb in verbs:
                verbHtmlContent += '''
                <li><h4>{0}</h4></li>
                '''.format(verb)


            adjectivesHtmlContent = "" if len(adjectives) == 0 else  '''<hr/>
            <h3>വിശേഷണം<span>:Adjective</span></h3>
            <hr/>'''
            for adjective in adjectives:
                adjectivesHtmlContent += '''
                <li><h4>{0}</h4></li>
                '''.format(adjective)
            


            adverbHtmlContent = "" if len(adverbs) == 0 else  '''
            <hr/>
            <h3>ക്രിയാവിശേഷണം<span> :Adverb</span></h3>
            <hr/>
            '''
            for adverb in adverbs:
                adverbHtmlContent += '''
                <li><h4>{0}</h4></li>
                '''.format(adverb)




            pronounHtmlContent = "" if len(pronouns) == 0 else  '''
            <hr/>
            <h3>സര്‍വ്വനാമം<span> :Pronoun</span></h3>
            <hr/>
            '''
            for pronoun in pronouns:
                pronounHtmlContent += '''
                <li><h4>{0}</h4></li>
                '''.format(pronoun)

            propernounHtmlContent = "" if len(properNouns) == 0 else  '''
            <hr/>
            <h3>സംജ്ഞാനാമം<span> :Proper noun</span></h3>
            <hr/>
            '''
            for propnoun in properNouns:
                propernounHtmlContent += '''
                <li><h4>{0}</h4></li>
                '''.format(propnoun)

            phrasalVerbHtmlContent = "" if len(phrasalVerbs) == 0 else  '''
            
            <hr/>
            <h3>ഉപവാക്യ ക്രിയ<span> :Phrasal verb</span></h3>
            <hr/>
            '''
            for phrasalVerb in phrasalVerbs:
                phrasalVerbHtmlContent += '''
                <li><h4>{0}</h4></li>
                '''.format(phrasalVerb)

            conjunctionHtmlContent = "" if len(conjunctions) == 0 else  '''
            
            <hr/>
            <h3>അവ്യയം<span>:Conjunction</span></h3>
            <hr/>
            '''
            for conjunction in conjunctions:
                conjunctionHtmlContent += '''
                <li><h4>{0}</h4></li>
                '''.format(conjunction)



            interjectionHtmlContent = "" if len(interjections) == 0 else  '''
            
            <hr/>
            <h3>വ്യാക്ഷേപകം<span> :interjection</span></h3>
            <hr/>
            '''
            for interjection in interjections:
                interjectionHtmlContent += '''
                <li>{0}</li>
                '''.format(interjection)

            prepositionHtmlContent = "" if len(prepositions) == 0 else  '''
            
            <hr/>
            <h3>വ്യാക്ഷേപകം<span> :preposition</span></h3>
            <hr/>
            '''
            for preposition in prepositions:
                prepositionHtmlContent += '''
                <li>{0}</li>
                '''.format(preposition)


            prefixHtmlContent = "" if len(prefixs) == 0 else  '''
            
            <hr/>
            <h3>പൂർവ്വപ്രത്യയം<span> :Prefix</span></h3>
            <hr/>
            '''
            for prefix in prefixs:
                prefixHtmlContent += '''
                <li>{0}</li>
                '''.format(prefix)



            suffixHtmlContent = "" if len(suffixs) == 0 else  '''
            
            <hr/>
            <h3>പ്രത്യയം<span> :Suffix</span></h3>
            <hr/>
            '''
            for suffix in suffixs:
                suffixHtmlContent += '''
                <li>{0}</li>
                '''.format(suffix)



            abbrHtmlContent = "" if len(abbreviations) == 0 else  '''
            
            <hr/>
            <h3>പ്രത്യയം<span> :Suffix</span></h3>
            <hr/>
            '''
            for abbr in abbreviations:
                abbrHtmlContent += '''
                <li>{0}</li>
                '''.format(abbr)


            auxiliaryVerbHtmlContent = "" if len(auxiliaryVerbs) == 0 else  '''
            
            <hr/>
            <h3>പൂരകകൃതി <span> :Auxiliary verb</span></h3>
            <hr/>
            '''
            for auxv in auxiliaryVerbs:
                auxiliaryVerbHtmlContent  += '''
                <li>{0}</li>
                '''.format(auxv)


            idiomsHtmlContent = "" if len(idioms) == 0 else  '''
            
            <hr/>
            <h3>പൂരകകൃതി <span> :Idioms</span></h3>
            <hr/>
            '''
            for idiom in idioms:
                idiomsHtmlContent  += '''
                <li>{0}</li>
                '''.format(idiom)


            htmlContent = '''

            <h3>Word : {0} </h3>
            <ul>


            {1}


            {2}

            {3}


            {4}


            {5}

            {6}

            {7}

            {8}

            {9}

            {10}


            {11}

            {12}


            {13}

            {14}


            {15}

            {16}

            </ul>

            '''.format(self.wordInput.text().strip(), meaningHtmlContent, nounHtmlContent, verbHtmlContent, adjectivesHtmlContent, 
                adverbHtmlContent, pronounHtmlContent, propernounHtmlContent, phrasalVerbHtmlContent, conjunctionHtmlContent,
                interjectionHtmlContent, prepositionHtmlContent, prefixHtmlContent, suffixHtmlContent, abbrHtmlContent, auxiliaryVerbHtmlContent,
                idiomsHtmlContent)
        return htmlContent

    def searchMeaning(self, word):
        results = self.nighandu.search_word(word)
        return results

    @pyqtSlot()
    def zoomIn(self):

        font = self.wordViewerLabel.font()
        fontSize = font.pixelSize()
        font.setPixelSize(fontSize+3)
        self.wordViewerLabel.setFont(font)

    @pyqtSlot()
    def zoomOut(self):

        font = self.wordViewerLabel.font()
        fontSize = font.pixelSize()
        font.setPixelSize(fontSize-3)
        self.wordViewerLabel.setFont(font)

    @pyqtSlot()
    def about(self):
        
        content = """
        <center>
        <h2> Nighandu </h2>
        <p>
        Nighandu is an free opensoure english malayalam dictionary software. <br/>
        This is based on <a href="https://olam.in/open/enml/">Olam English-Malayalam dictionary dataset</a>
        
        <br/>
        <br/>
        <br/>
        Project: https://github.com/Vivx701/Nighandu
        <br/>
        Developer: Vivek.P (https://github.com/Vivx701)
        <br/>
        </p>
        </center>
        """
        contentLayout = QHBoxLayout()
        contentLabel = QLabel(self)
        contentLabel.setText(content)
        contentLayout.addWidget(contentLabel)
        contentLayout.addStretch()
        dialog = QDialog(self)
        dialog.window().setWindowTitle("About")
        dialog.setLayout(contentLayout)
        dialog.exec()
        




if __name__ == "__main__":

    app = QApplication(sys.argv)
    nighanduGui = NighanduGui()
    nighanduGui.show()
    sys.exit(app.exec_())  