
import sys
import math
from string import ascii_lowercase

students = []
groups = []
studentsInGroup = []

# placeholders, negative for debugging until set
global numStudents
global numGroups

# range of how many students should be in each group, default
global minGroupSize
global maxGroupSize

"""
Java class

public class Student(int id){
    int id;
    int[] preferences;
    public Student(int id){
        this.id = id;
        this.preferences = new Array[]
      }
}
"""

# integer ID identifier and an ordered list of student's preferred groups
class Student:
    def __init__(self, id):
        self.ID = id
        self.prefers = []
        self.timestamp = 0
    
    def __init__(self, id, timestamp):
        self.ID = id
        self.prefers = []
        self.timestamp = timestamp
    
    # for reading in a test file that already provides preferences
    def __init__(self, id, prefers):
        self.ID = id
        self.prefers = prefers
        self.timestamp = 0
    
    def __init__(self, id, prefers, timestamp):
        self.ID = id
        self.prefers = prefers
        self.timestamp = timestamp

class Group:
    def __init__(self, id):
        self.ID = id
        self.size = 0
        self.students = []
        self.name = ""
    
    def __init__(self, id, name):
        self.ID = id
        self.size = 0
        self.students = []
        self.name = name

# calculates the min and max group size based on student to group ratio
def calculateGroupSizeRange():
    global numStudents
    global numGroups
    global minGroupSize
    global maxGroupSize

    # get the ratio of students to groups
    midSize = numStudents / numGroups

    # get 2 ints, 1 above and below ratio for max and min group size
    # if not an int
    if (numStudents % numGroups) != 0:
        #print("uneven distribution")
        minGroupSize = math.floor(midSize) - 1
        maxGroupSize = math.ceil(midSize)
    #endif
    # if the ratio of groups to students is even
    else:
        #print("even distribution")
        minGroupSize = midSize - 1
        maxGroupSize = midSize + 1

    

# function to find a specific student in a list of students
# false if student not in list, true if student in list
def studentSearch(studentToFind):
    if len(studentsInGroup) == 0:
        return False
    for student in studentsInGroup:
        if studentToFind.ID == student.ID:
            return True
    return False

# if a test file was included in the command line, use this to get the data
if len(sys.argv) > 1:
    # get filename from first argument
    fName = sys.argv[1]

    f = open(fName, 'r')
    # reads first line for 'course info', use strip to remove tailing '\n'
    currLine = f.readline().strip()
    # split by delimiter
    myNums = currLine.split(';', 1)

    numGroups = int(myNums[0])
    numStudents = int(myNums[1])

    # create group objs to add students to
    i = 0
    while i < numGroups:
        groups.append(Group(i, ascii_lowercase[i]))
        i += 1

    # start getting the students from the file
    # timestamp for students just in order they were added
    time = 0
    for line in f:
        #print(line.strip())
        # split by numGroups, in case 0 should be 3
        # also convert all elements to int, since starst as string after being read from file
        currLine = [int(i) for i in line.strip().split(';', numGroups)]
        currStudent = currLine[0]
        # access from index 1, stopping before numGroups + 1
        currPrefers = currLine[1:(numGroups+1)]

        students.append(Student(currStudent, currPrefers, time))
        time += 1

    f.close()

    # print debug
    for group in groups:
        print(group.ID, " ", group.name)
    print()
    for student in students:
        print(student.ID, " prefers: ", student.prefers)
    print()

    # end getting and formatting file data

    # calculates the min and max group size based on student to group ratio
    calculateGroupSizeRange()
    print("min:", minGroupSize, ", max:", maxGroupSize)
    print()

    # STEP 1: fill all groups until the minimum size is reached, starting with
    # students who have that group as their priority. once one level of priority
    # has been used
    preferIndex = 0         # incr until at last preference
    while len(studentsInGroup) < (numGroups * minGroupSize):
        print("filling groups 1")
        while preferIndex < numGroups:
            print("preference index ", preferIndex)
            for group in groups:
                print("group ", group.name)
                # if the group is not at min size, add students
                if group.size < minGroupSize:
                    print("group not full, adding students")
                    for student in students:
                        # check if student is already in a group, if not check preference
                        if studentSearch(student) == False:
                            if student.prefers[preferIndex] == group.ID:
                                group.students.append(student)
                                group.size += 1
                                studentsInGroup.append(student)
                        # if the group is now at min size, skip adding students
                        if group.size == minGroupSize:
                            break
                    # end student search to add loop
                    print("reached end of students")
            # end group loop
            print("reached end of groups")
            # check group sizes to see if can break loop
            preferIndex += 1
        # end incr prefer-index
    # end filling groups

    for group in groups:
        print(group.name, ": ")
        for student in group.students:
            print(student.ID, ": ", student.prefers)
        print()
    
    print("getting the rest of te students assigned")

    # STEP 2: once groups have all been ensured to have the minimum number of
    # students, now they can be filled until the rest of the students have been
    # placed in a group

    # until all students are in a group
    preferIndex = 0
    while len(studentsInGroup) < numStudents:
        while preferIndex < numGroups:
            for group in groups:
                # as long as the group isn't at max size
                if group.size < maxGroupSize:
                    for student in students:
                        if studentSearch(student) == False:
                            if student.prefers[preferIndex] == group.ID:
                                group.students.append(student)
                                group.size += 1
                                studentsInGroup.append(student)
                                break
                    # end student search
                # endif
            # end group loop
            preferIndex += 1
    # end student assignment

    # all students should be in groups now
    print(len(studentsInGroup), " in groups")
    for group in groups:
        print(group.name, ", size: ", group.size)
        for student in group.students:
            print(student.ID, ": ", student.prefers)
        print()
    
# endif
# otherwise if no file was included do nothing
else:
    print("file not given as arg, ending program")
