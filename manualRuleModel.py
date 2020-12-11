import os
import sys
import nltk

trainingFile = open("train.csv", 'r')
train = trainingFile.readlines()
trainingFile.close()

devFile = open("dev.csv", 'r')
dev = devFile.readlines()
devFile.close()

occured = {}
#diseaseName = [] for next step implementation, consider using UMLS REST API 
#add all B, BI (as a phrase) to occured
i=0
while i <len(train):
	train[i] = train[i].rstrip()
	entry = train[i].split(",")
	token = entry[3]
	BIO = entry[4]
	
	if BIO=="B-indications":
		temp = token
		j = i+1
		while j<len(train):
			tempAdd = train[j].rstrip().split(",")
			if tempAdd[4]=="I-indications":
				temp+= " "+tempAdd[3]
				j+=1
			else:
				break
		i = j
		if token in occured:
			if temp not in occured[token]:
				occured[token].append(temp)
		else:
			occured[token] = [temp]
	else:
		i+=1

i=0
while i<len(dev):
	dev[i] = dev[i].rstrip()
	entry = dev[i].split(",")
	token = "".join(entry[3:])
	if token in occured:
		#single word
		if token in occured[token]:
			dev[i]+=",B-indications\n"
			i+=1
		#not single word, check up to bi-gram
		else:
			tempStr= token
			flag = False
			for j in range(i+1,i+5):
				if j>=len(dev):
					break
				tempEntry = dev[j].rstrip()
				tempEntry = tempEntry.split(",")
				tempStr +=" "+ "".join(tempEntry[3:])
				if tempStr in occured[token]:
					#mark i as B and i+1-j as I
					for k in range(i,j+1):
						if k==i:
							dev[k]= dev[k].rstrip()
							dev[k]+=",B-indications\n"
						else:
							dev[k]=dev[k].rstrip()
							dev[k]+=",I-indications\n"
					flag = True
					break
			if flag ==True:
				i = j+1
			else:
				dev[i]+=",O\n"
				i+=1
	else:
		dev[i] +=",O\n"
		i+=1

#write ans
ansFile = open("BaselineResult.csv","w")
i=0
for i in range(len(dev)):
	ansFile.write(dev[i])
ansFile.close()









