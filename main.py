from fileinput import filename
from pyDF import *
import os
import time

sourcePath = str(os.path.dirname(os.path.realpath(__file__))) + "/sources"
savePath = "sortedFiles"

def sourcesList(sourcePath):
    sourceList = []
    for current, directories, files in os.walk(sourcePath):
        for f in files:
            sourceList.append(current + '/' + f)

    return sourceList

def getList(file):
    list = []
    with open(file) as tf:
        lines = tf.read().split(',')
        tf.close()

    for line in lines:
        list.append(line)

    return list
def saveList(list, splitedName):
    saveName = savePath + '/' + 'sorted_' + splitedName.split('.')[0] + '.txt'
    with open(saveName, 'w') as tf:
        for item in list:
            tf.write(item + ",")
        tf.close()
        

def sort(list):
    listLength = len(list)
    tempList = [0]*listLength
    mergeSort(list,tempList,0,listLength-1)

def mergeSort(list,tempList,start,end):
    if start < end:
        mid = (start + end) // 2
        mergeSort(list,tempList,start,mid)
        mergeSort(list,tempList,mid+1,end)
        merge(list,tempList,start,mid+1,end)

def merge(list,tempList,start,mid,end):
    endFirstPart = mid - 1
    tempIndex = start
    lenList = end - start + 1

    while start <= endFirstPart and mid <= end:
        if list[start] <= list[mid]:
            tempList[tempIndex] = list[start]
            start += 1
        else:
            tempList[tempIndex] = list[mid]
            mid += 1
        tempIndex += 1
    while start <= endFirstPart:
        tempList[tempIndex] = list[start]
        tempIndex += 1
        start += 1
    while mid <= end:
        tempList[tempIndex] = list[mid]
        tempIndex += 1
        mid += 1
    for i in range(0, lenList):
        list[end] = tempList[end]
        end -= 1

def saveSortedList(args):
    fileName = args[0]
    #fileName = sourcesList(sourcePath)[0]
    splitName = fileName.split('/')[-1]
    listsToSort = getList(fileName)
    sort(listsToSort)

    saveList(listsToSort, splitName)

    return listsToSort
    




def printSortedList(args):
    fileName = args[0];

    print("Sorted Files %s" %fileName)

def main(nprocs):

    sources = sourcesList(sourcePath)

    graph = DFGraph()
    scheduler = Scheduler(graph, nprocs, mpi_enabled = False)

    feedFiles = Source(sources)
    convertedFile = FilterTagged(saveSortedList,1)
    pname = Serializer(printSortedList,1)

    graph.add(feedFiles)
    graph.add(convertedFile)
    graph.add(pname)

    feedFiles.add_edge(convertedFile,0)
    convertedFile.add_edge(pname,0)

    t0 = time.time()
    scheduler.start()
    t1 = time.time()

    print("Time: %.3f" %(t1-t0))

main(int(sys.argv[1]))
# main(1)
