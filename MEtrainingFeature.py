
import nltk

trainingFile = open("train.csv", 'r')
train = iter(trainingFile)

bio_tag = []
sent_id = 1
sentence = []
tmp_s = []
pos_tag = []
tmp2 = []

for w in train:
    s = ''.join([i if ord(i) < 128 else ' ' for i in w]).strip()
    s1 = s.split('"')
    s2 = []
    if len(s1) == 1:
        s = s.split(',')
    else:
        s2.extend(s1[0].split(",")[0:3])
        s2.append(s1[1])
        s2.append(s1[2].split(",")[1])
        s = s2
    if int(s[2]) == sent_id:
        tmp_s.append(s[3])
        pos_tag.append(s[4])
    else:
        tmp = nltk.pos_tag(tmp_s)
        #print(tmp)
        for n, p in enumerate(pos_tag):
            tmp2 = list(tmp[n])
            tmp2.append(p)
            tmp[n] = tuple(tmp2)
        sentence.append(tmp)
        tmp_s = []
        pos_tag = []
        sent_id += 1
        tmp_s.append(s[3])    
        pos_tag.append(s[4])
       
tmp = nltk.pos_tag(tmp_s)
for n, p in enumerate(pos_tag):
    tmp2 = list(tmp[n])
    tmp2.append(p)
    tmp[n] = tuple(tmp2)
sentence.append(tmp)


def word2features(doc, i):
    word = doc[i][0]
    postag = doc[i][1]
    feature_list = []
    # stem = nltk.stem.PorterStemmer().stem(word)
    # Common features for all words
    features = [
        'token=' + word,
        'postag=' + postag,
        'word[-3:]=' + word[-3:],
        'word[-2:]=' + word[-2:],
        'cap=%s' % word.isupper(),
        'alpha=%s' % word.isalpha(),
        'numeric=%s' % word.isnumeric()
        # 'stem = %s', % stem
    ]

    # Features for words that are not
    # at the beginning of a document
    if i > 0:
        word1 = doc[i-1][0]
        postag1 = doc[i-1][1]
        features.extend([
            'PrevPos=' + postag1
        ])
    else:
        # Indicate that it is the 'beginning of a document'
        features.append('BOS=BOS')
    if i > 1:
        postag2 = doc[i-2][1]
        features.extend([
            'Prev2Pos=' + postag2
        ])

    # Features for words that are not
    # at the end of a document
    if i < len(doc)-1:
        word1 = doc[i+1][0]
        postag1 = doc[i+1][1]
        features.extend([
            'Nextpostag=' + postag1
        ])
    else:
        # Indicate that it is the 'end of a document'
        features.append('EOS=EOS')
    if i< len(doc)-2:
    	postag2 = doc[i+2][1]
    	features.extend([
            'Next2postag=' + postag2
        ])
    return features


# A function for extracting features in documents
def extract_features(doc):
    return [word2features(doc, i) for i in range(len(doc))]


# A function fo generating the list of labels for each document
def get_labels(doc):
    return [label[0] for (token, postag, label) in doc]


X = [extract_features(doc) for doc in sentence]
y = [get_labels(doc) for doc in sentence]

trainAns = open("training.feature","w")

for i in range(len(X)):
	for j in range(len(X[i])):
		cur = X[i][j]
		BIO = y[i][j]
		tempStr = "\t".join(cur)+"\t"
		prevBIO = ""
		prev2BIO = ""

		if j-1>0:
			prevBIO = "prevBIO="+y[i][j-1] +"\t"
		if j-2>0:
			prev2BIO = "prev2BIO="+ y[i][j-2]+ "\t"
		tempStr+= prevBIO + prev2BIO + BIO +"\n"
		trainAns.write(tempStr)
trainAns.close()
