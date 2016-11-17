#coding:utf-8
import numpy as np, copy
#import matplotlib.pyplot as plt
import math, operator

class DataLayer(object):
    def __init__(self, filename):
        self.filename = filename
        
    def loadDataSet(self):
        numFeat = len(open(self.filename).readline().split(' ')) - 1
        dataArr = []; labelArr = []; xJson = []; yJson = []; yDic = {}
        for i in open(self.filename).readlines():
            lineArr = []
            curLine = i.strip().split(' ')
            k=0; xDic = {};
            for j in range(numFeat):
                lineArr.append(float(curLine[j]))
                xDic['x'+str(k)] = float(curLine[j]); k+=1
            dataArr.append(lineArr); xJson.append(xDic)
            labelArr.append(float(curLine[-1]))
            yDic['y']=float(curLine[-1]); yJson.append(yDic.copy())
        return numFeat, dataArr, labelArr, xJson
        
class LinearRegression(object):       
    def __init__(self, xArr, yArr):
        self.xArr = xArr
        self.yArr = yArr
        self.xMat = np.mat(self.xArr)
        self.yMat = np.mat(self.yArr).T
    def _lr(self):    
        xTx = self.xMat.T * self.xMat
        if np.linalg.det(xTx) == 0.0:
            print('This matrix is singular, can not do inverse')
            return -1
        ws = xTx.I * (self.xMat.T * self.yMat)
        yHat = self.xMat * ws
        ws = [i[0] for i in ws.tolist()]
        y_predict = [i[0] for i in yHat.tolist()]
        rssE = rssError(self.yMat.A, yHat.A)
        return ws, y_predict, rssE        
        
    def train(self):
        ws, y_predict, rssE = self._lr()
        return ws, y_predict, rssE

class LocallyWeightedLinearRegression(object):
    def __init__(self, xArr, yArr):
        self.xArr = xArr
        self.yArr = yArr
        self.xMat = np.mat(self.xArr)
        self.yMat = np.mat(self.yArr).T
        
    def _lwlr_part(self, testPoint, k=1):
        m = np.shape(self.xMat)[0]
        weights = np.eye(m)
        for i in range(m):
            diffMat = testPoint - self.xMat[i]
            weights[i,i] = np.exp((diffMat*diffMat.T)/(-2.0*k**2))
        xTx = self.xMat.T * weights * self.xMat
        if np.linalg.det(xTx) == 0.0:
            print('This matrix is singular, cannot do inverse')
            return -1
        ws = xTx.I * self.xMat.T * weights * self.yMat
        return testPoint * ws
      
    def _lwlr(self, testArr, k=1):
        m = np.shape(testArr)[0]
        yHat = np.zeros((m, 1))
        for i in range(m):
            yHat[i] = self._lwlr_part(testArr[i], k=k)
        return yHat
        
    def train(self):
        ws = [None for i in range(len(self.xArr[0]))]
        yHat = self._lwlr(self.xArr, k=1)
        y_predict = [i[0] for i in yHat.tolist()]
        rssE = rssError(self.yMat.A, yHat)
        return ws, y_predict, rssE
     
class LogisticRegression(object):   
    def __init__(self, xArr, yArr):
        self.xArr = xArr
        self.yArr = yArr
        self.xMat = np.mat(self.xArr)
        self.yMat = np.mat(self.yArr).T
    def _lwlr(self):
        m, n = np.shape(self.xMat)
        ws = np.ones((1, n))
        alpha = 0.01
        for i in range(m):
            h = sigmoid(np.sum(np.array(self.xMat[i]) * ws))
            error = self.yArr[i] - h
            ws = ws + alpha * error * np.array(self.xArr[i])
        yHat = np.zeros((m, 1))
        for i in range(m):
            yHat[i] = sigmoid(np.sum(self.xArr[i] * ws))
        y_predict = [i[0] for i in yHat.tolist()]
        rssE = rssError(np.array(self.yArr), yHat)
        return ws[0].tolist(), y_predict, rssE
    def train(self):
        ws, y_predict, rssE = self._lwlr()
        return ws, y_predict, rssE
        
        
def whichAlgo(xArr, yArr, algo):
    xMat = np.mat(xArr); yMat = np.mat(yArr).T
    if algo == 'lr':
        lr = LinearRegression(xArr, yArr)
        ws, y_predict, rssE = lr.train()
        return ws, y_predict, rssE
    elif algo == 'lwlr':
        lwlr = LocallyWeightedLinearRegression(xArr, yArr)
        ws, y_predict, rssE = lwlr.train()
        return ws, y_predict, rssE
    elif algo == 'lrlr':
        lrlr = LogisticRegression(xArr, yArr)
        ws, y_predict, rssE = lrlr.train()
        return ws, y_predict, rssE
    elif algo == 'dt':
        ws = [None for i in range(len(xArr[0]))]
        y_predict = [None for i in range(len(yArr))]
        dataAll = []
        for i in range(len(yArr)):
            tmp = copy.deepcopy(xArr[i])
            tmp.append(yArr[i])
            dataAll.append(tmp)
        labels = ['x'+str(i) for i in range(len(xArr[0]))]
        myTree = createTree(dataAll,labels)  
        rssE = []
        rssE.append(str(myTree))
        return ws, y_predict, rssE
          
def rssError(yArr, yHat):
    return ((yArr-yHat)**2).sum()

def sigmoid(z):
    return 1.0 / (1 + np.exp(-z))
    
'''
def Plot(xArr, yArr, ws):
    xMat = np.mat(xArr);yMat = np.mat(yArr).T
    wsMat = np.mat(ws)
    yHat = xMat * wsMat
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xMat[:,1].flatten().A[0], yMat[:,0].flatten().A[0])
    ax.plot(xMat[:,1], yHat)
    ax.set_title('lr')
    fig.savefig('static/lr.jpg')

    yHat = lwlr(xArr, xArr, yArr, k=0.01)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xMat[:,1].flatten().A[0], yMat[:,0].flatten().A[0] ,c='red')
    ax.scatter(xMat[:,1], yHat, 'r')
    ax.set_title('lwlr')
    fig.savefig('static/lwlr.jpg')
''' 

  

'''    
#algo == 'lwlr'
def lwlr_part(testPoint, xArr, yArr, k=1):
    xMat = np.mat(xArr); yMat = np.mat(yArr).T
    m = np.shape(xMat)[0]
    weights = np.eye(m)
    for i in range(m):
        diffMat = testPoint - xMat[i]
        weights[i,i] = np.exp((diffMat*diffMat.T)/(-2.0*k**2))
    xTx = xMat.T * weights * xMat
    if np.linalg.det(xTx) == 0.0:
        print('This matrix is singular, cannot do inverse')
        return -1
    ws = xTx.I * xMat.T * weights * yMat
    return testPoint * ws

def lwlr(testArr, xArr, yArr,k=1):
    m = np.shape(testArr)[0]
    yHat = np.zeros((m, 1))
    for i in range(m):
        yHat[i] = lwlr_part(testArr[i], xArr, yArr, k=k)
    return yHat
'''
    
    
#algo == 'dt'  
def calcShannonEnt(dataSet):
    numEntries = float(len(dataSet))
    labelCounts = {}
    for featVec in dataSet: 
        currentLabel = featVec[-1]
		#下面2句可以用labelCounts[currentLabel]=labelCounts.get(currentLabel,0)+1代替
        if currentLabel not in labelCounts.keys(): labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0
    for key in labelCounts:
        prob = labelCounts[key]/numEntries
        shannonEnt -= prob * math.log(prob,2)
    return shannonEnt
	
#生成表：从表dataSet的第axis列的属性=value的记录
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]    
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet
    
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1      
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0;bestFeature = -1                     
    for i in range(numFeatures):    
        featList = [example[i] for example in dataSet]    #表dataSet的每一个list的第i个组成list
        uniqueVals = set(featList)     
        newEntropy = 0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/len(dataSet)
            newEntropy += prob * calcShannonEnt(subDataSet)     
        infoGain = baseEntropy - newEntropy     
        if (infoGain > bestInfoGain):       
            bestInfoGain = infoGain       
            bestFeature = i
    return bestFeature                     #返回最大信息增益的属性所在的列

#对响应变量计数，返回出现最多的响应变量值
def majorityCnt(classList):
    classCount={}
    for vote in classList:
	    #下面2行可以用代替classCount[vote]=classCount.get(vote,0)+1
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList): 
        return classList[0]#stop splitting when all of the classes are equal
    if len(dataSet[0]) == 1: #stop splitting when there are no more features in dataSet
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]       #copy all of labels, so trees don't mess up existing labels
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value),subLabels)
    return myTree
    
#algo == 'nb'

