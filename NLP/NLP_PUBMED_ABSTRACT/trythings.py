results = ["aaa", "hbbb", "cccc"]
stringResults = 'a'
stringResults = ''.join(res+"\n" for res in results)
print(stringResults)

import nltk
stopwords = nltk.corpus.stopwords.words('english')
punctuation = [',','.',';']
print(punctuation)
