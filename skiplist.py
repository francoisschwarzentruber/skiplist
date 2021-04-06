from random import randint, seed

# a bus stop represents an element.
#       busStop.value is the element
#       busStop.next is an array of pointers
#           BusStop.next[i] is the pointer of line i to the next bus stop
#           line 0 = line with *all* stops
#           line 1 = express line
#           line 2 = express express line
#           etc.
class BusStop:
    #input: value = value of the element
    #        nbLines : number of pointers to be allocated
    def __init__(self, nbLines, value):
        self.value = value
        self.next = [None]*nbLines
        
    #input: nbLines : number of lines
    #result: allocate new lines if needed, existing lines keep unchanged
    def allocate(self, nbLines):
        while len(self.next) < nbLines:
            self.next.append(None)
       
    #returns the number of lines that go throw this bus stop
    @property
    def nbLines(self): return len(self.next);


#class for the data structure
class SkipList:
    def __init__(self):
        self.sentinel = BusStop(0, '-∞') #first element is a sentinel
        self.nbLines = 0

    #returns, for all lines, the bus stops that are just before the value
    #for that, it performs the walk of Skippy (see the video)
    def getBusStopsJustBefore(self, value):
        stops = [None]*self.nbLines
        x = self.sentinel
        for i in reversed(range(self.nbLines)):
            #invariant: x.value < value
            while x.next[i] != None and x.next[i].value < value:
                x = x.next[i]
            stops[i] = x
        return stops
    
#precondition: the list must be non empty
#value = the value to be found
#stopsJustBefore (optional) = the stops just before without exceeding
#        or being equal to the value
#
#if the skip list contains the element
#      returns the bus stopsuch that BusStop.element == element
#otherwise
#      returns None
    def find(self, value, stopsJustBefore = None):
        if stopsJustBefore == None:
            stopsJustBefore = self.getBusStopsJustBefore(value)
        
        busStop = stopsJustBefore[0].next[0]
        if busStop != None and busStop.value == value:
            return busStop
        else:
            return None
      
    #precondition: the value should not be already in the skip list
    #add a value in the skip list
    def insert(self, value):

        #computes a randomly promoted bus stop for value
        def computePromotedBusStop(value):
             height = 0
             while randint(1, 2) != 1:
                  height += 1
             return BusStop(1+height, value)
    
        newStop = computePromotedBusStop(value)

        
        self.nbLines = max(self.nbLines, newStop.nbLines)
        self.sentinel.allocate(self.nbLines)
        stopsJustBefore = self.getBusStopsJustBefore(value)
        
        #insert the new stop in all the bus lines
        for i in range(len(newStop.next)):
             newStop.next[i] = stopsJustBefore[i].next[i]
             stopsJustBefore[i].next[i] = newStop

    #remove the value in the skip list
    def remove(self, value):
        stopsJustBefore = self.getBusStopsJustBefore(value)
        busStop = self.find(value, stopsJustBefore)
        if busStop != None:
            #remove the bus stop in the list
            for i in reversed(range(len(busStop.next))):
                stopsJustBefore[i].next[i] = busStop.next[i]
                if self.sentinel.next[i] == None:
                    self.nbLines -= 1

#print the content of the skiplist in the console (ASCII art)
    def __str__(self):
        S =[""]*self.nbLines;
        X=[self.sentinel]*self.nbLines;
        x = self.sentinel
        
        while x != None:
            for i in range(len(self.sentinel.next)-1, 0, -1):
                if X[i] == x:
                    S[i] += "-> " + str(x.value) + " "
                    X[i] = X[i].next[i]
                else:
                    S[i] += "-"*(len(str(x.value))+4)
            S[0] += "-> " + str(x.value) + " "
            x = x.next[0]
            
            
        s = ""
        for i in range(len(self.sentinel.next)-1, -1, -1):
            s += S[i] + "\n\n\n";
            
        return s



#Example of use

L = SkipList()
for i in range(10):
    if(randint(1, 2) != 1):
           L.insert(i)
   
print(L)
