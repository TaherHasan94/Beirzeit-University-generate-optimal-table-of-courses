import json
class Course:
    def __init__(self, course_label, section, instructor, days, time_display, place=None, numOfStudents=None):
        self.course_label = course_label
        self.time_display = time_display  # 8:00-9:15
        self.section = section  # 0,1,2,3,...
        self.instructor = instructor  # name
        self.days = days  # "S,M,T,W,R" capital letters with comma
        self.place = place  # "O.Abdulhadi052"
        self.numOfStudents = numOfStudents  # 54 / 120

    def time_start(self):  # return string
        if self.time_display.split("-")[0] != "N/A":
            return self.time_display.split("-")[0]
        return "0:0"

    def time_end(self):  # return string
        if self.time_display.split("-")[0] != "N/A":
            return self.time_display.split("-")[1]
        return "0:0"

    def collision(self, other):  # other is another Course object
        # return True if self and other have collision
        flag_days = True  # keep True if no days in common

        for day in self.days.split(","):
            if day in other.days.split(","):
                flag_days = False
        if flag_days:  # no days in common

            return False
        if float(self.time_start().replace(":", ".")) >= float(other.time_end().replace(":", ".")):
            return False
        if float(self.time_end().replace(":", ".")) <= float(other.time_start().replace(":", ".")):
            return False
        return True

    def __str__(self):
        return f"{self.course_label}#{self.section}#{self.instructor}#{self.days}#{self.time_start()}#{self.time_end()}"

    def __repr__(self):
        return f"{self.course_label}#{self.section}#{self.instructor}#{self.days}#{self.time_start()}#{self.time_end()}"


# ------------------ Adding courses ------------------
def search_courses(course_name, preName):  # ex : preName = 'ACCT'
    found_courses = []
    flagWeGotOne = False
    try:
        with open(f'coursesJSON/{preName}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

            for course_data in data:
                if course_data["name of course"] == course_name:
                    flagWeGotOne = True
                    course = Course(
                        course_data["name of course"],
                        course_data["sec"],
                        course_data["name of instructor"],
                        course_data["days"].replace(" ", ""),
                        course_data["time"],
                        course_data["place"],
                        course_data["number of students"]
                    )

                    found_courses.append(course)
                elif flagWeGotOne:
                    break
        return found_courses
    except:
        return "preName not found"

#
# listACCT = search_courses("ENCS3320", "ENCS")
# listCOMP = search_courses("ENCS3330", "ENCS")
# listCOMP2 = search_courses("ENCS3340", "ENCS")
# listENCS = search_courses("ENCS4370", "ENCS")
# listENCS1 = search_courses("ENCS3130", "ENCS")
# listENCS2 = search_courses("ENCS3310", "ENCS")
# listENCS3 = search_courses("ENCS4110", "ENCS")
courses =[]
while True:
    print("Enter the course name example ENCS3320 or press X to go : ")
    courseName = input().upper()
    if courseName.upper() == "X":
        break
    elif len(courseName) < 4:
        continue
    else:
        preName = courseName[:4]
        if preName == "end":
            break
        course = search_courses(courseName,preName)
        if len(course) == 0:
            print("No course found")
            continue
        elif course == "preName not found":
            print("preName not found")
            continue
        else:
            courses.append(course)
            print(f"we got {len(course)} sections of {courseName}")

# courses = [listACCT, listCOMP, listCOMP2, listENCS, listENCS1, listENCS2, listENCS3]

# ------------------ preparing combinations ------------------

dec = {}


def combinations(ArraySec, index=0, current_combination=[]):

    if index == len(ArraySec):
        chosenSections = []
        for sec in range(len(current_combination)):  # making list of chosen sections
            chosenSections.append(courses[sec][current_combination[sec]])
            # example : chosenSections =  [<__main__.Course object at 0x000002B2EF867FD0>, <__main__.Course object at 0x000002B2EF867D90>]
        numberOfDays = []
        # check if there is a collision between chosen sections
        # current_combination = [0, 0] -> chosenSections = [arab1, eng1]
        # current_combination = [0, 1] -> chosenSections = [arab1, eng2]

        for i in range(len(chosenSections)):
            for day in chosenSections[i].days.split(','):  # check the days of each section
                if day not in numberOfDays:
                    numberOfDays.append(day)
            for j in range(i + 1, len(chosenSections)):
                if chosenSections[i].collision(chosenSections[j]):
                    return
        startTime = None
        endTime = None
        for section in chosenSections:
            if startTime == None or float(section.time_start().replace(":", ".")) < float(startTime.replace(":", ".")):
                startTime = section.time_start()
            if endTime == None or float(section.time_end().replace(":", ".")) > float(endTime.replace(":", ".")):
                endTime = section.time_end()


        chosenSectionsTuple = tuple(chosenSections)

        dec[chosenSectionsTuple] = {"numberOfDays": numberOfDays, "startTime": startTime, "endTime": endTime , "totalTime": str(float(endTime.replace(":", ".")) - float(startTime.replace(":", ".")))}
        return

    max_number = len(ArraySec[index]) - 1
    for i in range(max_number + 1):
        current_combination.append(i)
        combinations(ArraySec, index + 1, current_combination)
        current_combination.pop()

combinations(courses)


from GUI.interface import *
while True:
    input("courses has been saved press Enter to continue : ")
    flagReducedays = input("Do you want to reduce the days ? (y/n) : ")
    flagreduceTime = input("Do you want to reduce shift between lectures  ? (y/n) : ")
    flagReduceStartTime = input("Do you want to reduce the start time ? (y/n) : ")
    flagReduceEndTime = input("Do you want to reduce the end time ? (y/n) : ")
    if flagReducedays.upper() == "Y":
        flagReducedays = True
    else:
        flagReducedays = False
    if flagreduceTime.upper() == "Y":
        flagreduceTime = True
    else:
        flagreduceTime = False
    if flagReduceStartTime.upper() == "Y":
        flagReduceStartTime = True
    else:
        flagReduceStartTime = False
    if flagReduceEndTime.upper() == "Y":
        flagReduceEndTime = True
    else:
        flagReduceEndTime = False

    print(f"flagReducedays = {flagReducedays} \nflagreduceTime = {flagreduceTime} \nflagReduceStartTime = {flagReduceStartTime} \nflagReduceEndTime = {flagReduceEndTime} ")
    print("------------------------------------------------------------------------------------------------------------------------")
    display(DectoUse=dec,flagReducedays=flagReducedays,flagreduceTime=flagreduceTime,flagReduceStartTime=flagReduceStartTime,flagReduceEndTime=flagReduceEndTime)


# here we send the dec with all groups of sec that dont has any collision
