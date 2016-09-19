#!/usr/bin/python

from math import log
import operator

def createDataSet():
    dataSet = [[1,1,'yes'],
            [1,1,'yes'],
            [1,0,'no'],
            [0,1,'no'],
            [0,1,'no']];
    labels = ['no surfacing', 'flippers'];
    
    return dataSet, labels;

def calcShannonEnt( dataSet ):
    numEntries = len(dataSet );
    labelCounts = {};
    
    for featVec in dataSet:
        currentLabel = featVec[-1];

        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0;
        labelCounts[currentLabel] += 1;

    shannonEnt = 0.0;
    for key in labelCounts:
        prob = float( labelCounts[key]) / numEntries;
        shannonEnt -= prob * log(prob,2);

    return shannonEnt;

def splitDataSet( dataSet, axis, value ):
    retDataSet = [];
    
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis];
            reducedFeatVec.extend(featVec[axis+1:]);
            retDataSet.append( reducedFeatVec );

    return retDataSet;

def chooseBestFeatureToSplit( dataSet ):
    numFeatures = len(dataSet[0]) - 1;
    baseEntropy = calcShannonEnt( dataSet );
    bestInfoGain = 0.0; bestFeatrue = -1;

    for i in range(numFeatures):
        featList = [example[i] for example in dataSet ];
        uniqueVals = set(featList);
        newEntropy = 0.0;
        for value in uniqueVals:
            subDataSet = splitDataSet( dataSet, i,value );
            prob = len(subDataSet) / float(len(dataSet));
            newEntropy += prob*calcShannonEnt(subDataSet);

        infoGain = baseEntropy - newEntropy;
        if( infoGain > bestInfoGain ):
            bestInfoGain = infoGain;
            bestFeatrue = i;

    return bestFeatrue;

def majorityCnt( classList ):
    classCount = {};
    for vote in classList:
        if vote not in classCount.keys(): 
            classCount[vote] = 0;

        classCount[vote] += 1;

    sortedClassCount = sorted( classCount.iteritems(), key=operator.itemgetter(1), reverse=True );
    #print sortedClassCount;

    return sortedClassCount[0][0];

def createTree( dataSet, labels ):
    classList = [example[-1] for example in dataSet ];
    #print 'classList: '
    #print classList;
    #print classList.count( classList[0] );

    if classList.count( classList[0] ) == len(classList):
        return classList[0];
    if len(dataSet[0]) == 1:
        return majorityCnt(classList );
    bestFeat = chooseBestFeatureToSplit( dataSet );
    #print bestFeat;
    bestFeatLabel = labels[bestFeat];
    myTree = {bestFeatLabel:{}};
    del(labels[bestFeat]);
    featValues = [example[bestFeat] for example in dataSet ];
    uniqueVals = set(featValues);

    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree( splitDataSet(dataSet,bestFeat,value), subLabels );

    return myTree;
