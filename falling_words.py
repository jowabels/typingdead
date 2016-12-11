class Word:

  def getListOfWords(self):
    textFile = open("words.txt")
    listOfWords = []
    for word in textFile:
      word = word.strip()
      listOfWords.append(word)
    textFile.close()
    return listOfWords

