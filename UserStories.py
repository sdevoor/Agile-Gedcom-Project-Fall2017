import datetime
from Parser import individualTable, familyTable
from Functions import checkDate


def userStories(individualList, familyList):


    outputFile = open('Parser_Output.txt', 'a')
    outputFile.write('\n' + "{0:^150}".format(" Error Report ") + '\n' + '\n')
    outputFile.write('\t' + 'Tag' + '\t' + '\t' + 'Concerned' + '\t' + '\t' + 'User Story' + '\t' + '\t' + '\t' + 'Description' + '\t' + '\t' + '\t' + '\t' + '\t' +  '\t' + 'Location' + '\n' +'\n')
    outputFile.close()

 
    # Sprint 1 stories:
    individualAge(individualList)
    checkBigamy(individualList, familyList)
    birthBeforeMarriage_us02(individualList)
    birthBeforeDeath_us03(individualList)

########################################################################################################################################################################


def individualAge(individualList):
    """ US27 : Include individual ages """ 
    tag = "INFORMATION"
    concerned = "INDIVIDUAL"
    name = "US27"
    description = "List each individual's age"

    for indi in individualList:
        birth = individualList[indi].getBirthday().split("-")

        birthyear = int(birth[0])
        birthmonth = int(birth[1])
        birthdate = int(birth[2])

        today = datetime.date.today()

        age = today.year - birthyear
        if (today.month < birthmonth):
            age -= 1;
        elif (today.month == birthmonth):
            if (today.day < birthdate):
                age -= 1;


        individualList[indi].setAge(age)
        errorMessage(tag, concerned, name, description, indi + " - " + str(age))

#########################################################################################################################################################################


def checkBigamy(individualList, familyList):
    """ US11 : No bigamy """

    tag = "ERROR"
    concerned = "INDIVIDUAL"
    name = "US11"
    description = "Bigamy has been detected"

    for indi in individualList:
        if (individualList[indi].spouseFamily != 'NA'):   # Exclude the un-married people
            for fam in familyList:
                # Enter only if the person is a spouse in any other family apart from the one he/ she is currently a spouse in.
                if (fam != individualList[indi].spouseFamily and (individualList[indi].ID == familyList[fam].husband or individualList[indi].ID == familyList[fam].wife)):

                    firstMarriage = familyList[individualList[indi].spouseFamily]
                    secondMarriage = familyList[fam]
                    # Check for the first and second marriages depending on the marriage dates
                    if (checkDate(firstMarriage.marriage, secondMarriage.marriage) == False):
                        temp = firstMarriage
                        firstMarriage = secondMarriage
                        secondMarriage = temp

                    # Check if the person got married 2nd time even when he/ she has not yet been divorced from the 1st marriage
                    if (firstMarriage.divorce == 'NA'):
                        # Then check if the spouse from the 1st marriage is still alive for bigamy to take place
                        if (individualList[indi].ID == firstMarriage.husband):
                            if (isAlive(individualList[firstMarriage.wife])):
                                #bigamy = True       
                                errorMessage(tag, concerned, name, description, "in " + firstMarriage.ID + " and " + secondMarriage.ID + " by " + indi)
                        elif (individualList[indi].ID == firstMarriage.wife):
                            if (isAlive(individualList[firstMarriage.husband])):
                                #bigamy = True    
                                errorMessage(tag, concerned, name, description, "in " + firstMarriage.ID + " and " + secondMarriage.ID + " by " + indi)
                        
                    # Otherwise check if the person was once invloved in bigamy
                    else:
                        # If the person got divorced from 1st marriage after marrying the 2nd time
                        if (checkDate(secondMarriage.marriage, firstMarriage.divorce)):
                            #bigamy = True
                            errorMessage(tag, concerned, name, description, "in " + firstMarriage.ID + " and " + secondMarriage.ID + " by " + indi)

###########################################################################################################################################################################


def isAlive(person):
    """ Function to check if a person is still alive
        ** Not a user story """
    if (person.death != 'NA'):
        return False
    else:
        return True

###########################################################################################################################################################################



def birthBeforeMarriage_us02(individualList):
    tag="ERROR"
    concerned="INDIVIDUAL"
    US="US02"
    description=""
    location=""
    for indi in individualList:
        #print(" INDI "+indi+ "  marriage: "+marriage +" birth: "+birth)
        birthday= individualList[indi].getBirthday()
        marriage= individualList[indi].getMarriage()
        #print(" INDI "+indi+ "  marriage: "+marriage +" birth: "+birthday)
        if marriage == 'NA' and birthday !='':
            #pass this as it is ok
            continue
        elif birthday == '':
            #log this as error
            description="birthdate not specified"
            errorMessage(tag, concerned, US, description, indi)
            continue
        else:
            res=checkDate(birthday,marriage)
            if res!= True:
                #log this as error
                description="marriage "+ marriage+" is before dirthdate "+birthday
                errorMessage(tag, concerned, US, description, indi)
                #print("INDI "+indi+" NOT ok for marriage")
	
	
def birthBeforeDeath_us03(individualList):
    tag="ERROR"
    concerned="INDIVIDUAL"
    US="US03"
    description=""
    location=""
    for indi in individualList:
        birthday=individualList[indi].getBirthday()
        death=individualList[indi].getDeath()
        #print(" INDI "+indi+ "  death: "+death +" birth: "+birthday)
        if death == 'NA' and birthday != '':
            #pass this as it is okay
            #print ("INDI "+indi +" ok for death")
            continue
        if birthday == '':
            #log this as error
            #print ("INDI "+indi+" NOT ok for death")
            description="birthdate not specified"
            errorMessage(tag, concerned, US, description, indi)
            continue
        else:
            res=checkDate(birthday,death)
            if res!= True:
                #log this as error
                #print ("INDI "+ indi+" NOT ok for death")
                description="death "+ death+" is before dirthdate "+birthday
                errorMessage(tag, concerned, US, description, indi)
	

########################################################################################################################################################################
def US09_birthBeforeDeath(individualList, familyList):
    for i in range(len(familyList)):
        father_id = familyList[i][husband]
        mother_id = familyList[i[wife]]
    
#########################################################################################################################################################################
def errorMessage(tag, concerned, name, description, location = '-'):
    outputFile = open('Parser_Output.txt', 'a')
    outputFile.write(tag + '\t' + '\t' + concerned + '\t' + '\t' + name + '\t' + '\t' + '\t' + description + '\t' + '\t' + '\t' + '\t' + location + '\n')
    outputFile.close()
