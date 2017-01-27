
import sys
import unicodecsv

class Nighandu(object):

    def __init__(self, dataset_path):

        self.data_set = self.load_dataset(dataset_path)

    def load_dataset(self, path):
        data_set = dict()
        with open(path, 'rb') as f:
            reader = unicodecsv.DictReader(f, delimiter='\t')
            try:
                for row in reader:
                    if row['english_word'] in data_set:
                        data_set[row['english_word']].append(row)
                    else:
                        data_set[row['english_word']] = [row]

            except unicodecsv.Error as e:
                sys.exit('file %s, line %d: %s' % (path, reader.line_num, e))

        return data_set

    def search_word(self, english_word):
        if english_word in self.data_set:

            return self.data_set[english_word]
        else:
            return None

    def word_list(self):
        return self.data_set.keys()





def main():

    nighandu = Nighandu("olam-enml.csv")
    if len(sys.argv) < 2:
        print("Pass word as argument")
    else:

        results = nighandu.search_word(sys.argv[1])
        if results == None:
            print("No result found")
            return
        txt = ""
        for result in results:
            txt = txt+(result['malayalam_definition']+"\n")
        print(txt)
 

if __name__ == '__main__':
    main()



