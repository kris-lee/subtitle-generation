# utils for quick codeing
# auth : Zhu Hongji
# data : 2015-07-29

import codecs
import numpy as np
import os
import sys
import re
import datetime

def mkdir(path):
	import os

#	path=path.strip()
#	path=path.rstrip("\\")

	isExists=os.path.exists(path)
	if not isExists:
		print path+' create success'
		os.makedirs(path)
		return True


def ComputeEduDis(QueryFeature,SampleFeature):
	if QueryFeature.size != SampleFeature.size:
		print 'error: feature size not equal'
		return 0.0

	nDis= 0.0
	for i in range(QueryFeature.size):
		diff = (SampleFeature[i] - QueryFeature[i])
		nDis += diff*diff
	nDis = nDis / QueryFeature.size

	return nDis

def distance_one2all(qfeature, sfeatureData):
	nSampleNum = sfeatureData.shape[0]
	QSDistance  = np.zeros(nSampleNum)
	QSDistance  = QSDistance.astype('float32')
	for i in range(nSampleNum):
		#print qfeature.shape, sfeatureData[i].shape
		QSDistance[i] = ComputeEduDis(qfeature, sfeatureData[i]) 
	return QSDistance

def nsmallest(a,N):
	return np.argsort(a)[:N]

def nMaximum(a,N):
	return np.argsort(a)[-N:][::-1]

def sort_distance(QSDistance,topNum):
	nNum = QSDistance.shape[0]
	if nNum < topNum:
		topNum = nNum
		
	topidlist = nsmallest(QSDistance, topNum)
	return topidlist
def sort_distance_max(QSDistance,topNum):
	nNum = QSDistance.shape[0]
	if nNum < topNum:
		topNum = nNum
		
	topidlist = nMaximum(QSDistance, topNum)
	return topidlist

def simility(net ,qimg,simg):
	#print 'qimg: ',qimg 
	#print 'simg: ',simg 
	f1 = calFeature(net,qimg).copy()
	f2 = calFeature(net,simg).copy()
	
	dist = ComputeEduDis(f1,f2)
	print simg,': ',dist

def similityBatch(ClassifierNet,qimg,Path):
	nNum = 0
	for image in sorted(os.listdir(Path)):
		if image.lower().endswith(('.jpg','jpeg')):
			fullName    = Path + '/' + image
			#print fullName
			simility(ClassifierNet, qimg,fullName)			
			nNum = nNum + 1


def getImageList(Path):
	Path = Path.rstrip('/')
	
	listFileUri = Path +'_imglist.txt'
	imgList=[]
	if not os.path.isfile(listFileUri): 
		listfile = open(listFileUri,"w")
		nNum = 0
		for image in sorted(os.listdir(Path)): 
			if image.lower().endswith(('.jpg','jpeg')):
				fullName    = Path +'/'+ image
				if nNum%100 == 0:
					print str(nNum)+' '+fullName
				listfile.write(fullName+"\n")
				imgList.append(fullName)
				nNum = nNum + 1
		listfile.close()
		if nNum == 0:
			print 'no image found, remove imglist.txt'
			os.remove(listFileUri)
	else:
		listfile = open(listFileUri,"r")
		for line in listfile :
			imgList.append(line.strip('\n'))
		listfile.close()
	
	return imgList

def getImageListRecursive(Path):
	Path = Path.rstrip('/')
	
	listFileUri = Path +'_imglist.txt'
	imgList=[]
	if not os.path.isfile(listFileUri): 
		listfile = open(listFileUri,"w")
		nNum = 0
		for root,dirs,files in os.walk(Path):
			for image in files: 
				if image.lower().endswith(('.jpg','jpeg')):
					fullName    = os.path.join(root,image)
					if nNum%100 == 0:
						print str(nNum)+' '+fullName
					listfile.write(fullName+"\n")
					imgList.append(fullName)
					nNum = nNum + 1
		listfile.close()
		if nNum == 0:
			print 'no image found, remove imglist.txt'
			os.remove(listFileUri)
	else:
		print 'found imglist.txt, reading from file'
		listfile = open(listFileUri,"r")
		for line in listfile :
			imgList.append(line.strip('\n'))
		listfile.close()
	
	return imgList

def loadImageList(listFileUri):
	
	imgList=[]
	if os.path.isfile(listFileUri): 
		print 'found imglist.txt, reading from file'
		listfile = open(listFileUri,"r")
		for line in listfile :
			imgList.append(line.strip('\n'))
		listfile.close()
	else:
		print 'imglist no found',listFileUri
	return imgList
