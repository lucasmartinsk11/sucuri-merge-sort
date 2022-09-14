from fileinput import filename
from flask import Flask
from pyDF import *
import os
import time

app = Flask(__name__)


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

def selectionSort(array, size):
    
    for ind in range(size):
        min_index = ind
 
        for j in range(ind + 1, size):
            # select the minimum element in every iteration
            if array[j] < array[min_index]:
                min_index = j
         # swapping the elements to sort the array
        (array[ind], array[min_index]) = (array[min_index], array[ind])     

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
    # sort(listsToSort)
    selectionSort(listsToSort, len(listsToSort))

    saveList(listsToSort, splitName)

    return listsToSort
    




def printSortedList(args):
    fileName = args[0];

    print("Sorted Files %s" %fileName)

@app.route('/<nprocs>')
def main(nprocs):
    
    nprocs = int(nprocs)

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
    return "Time: %.3f" %(t1-t0)

# main(int(sys.argv[1]))
# main(1)

