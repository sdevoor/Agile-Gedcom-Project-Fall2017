from datetime import datetime
from datetime import date
from prettytable import PrettyTable
from Functions import writeTableToFile, checkDate, dates_within
from OutputValues import OutputValues
from datetime import timedelta

errorTable = PrettyTable()
errorTable.field_names = ['Tag','Concerned', 'User Story', 'Description', 'Location/ ID']

outputValues = OutputValues()
outputFile = ""

def sprint4(individualList, familyList):
    print "sprint4"

    for indi in individualList:
            #User story 32
           if list_multipe_births_US32(individualList,individualList[indi])is not True:
            for location in outputValues.location:
                errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,location])

           if List_upcoming_birthdsy_US38(individualList[indi]) is not True:
            for location in outputValues.location:
                errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,location])

 
   
    for fam in familyList:
    	family = familyList[fam]
    	if (correspondingEntries_us26(family, individualList)):
    		for location in outputValues.location:
    			errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,location])

    	orderSiblings_us28(family, individualList)
    	errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,outputValues.location])   		

        if checkDivorceBeforeDeath_us06(family,individualList[family.wife]) is not True:
            errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,family.wife])
        if checkDivorceBeforeDeath_us06(family,individualList[family.husband]) is not True:
            errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,family.husband])
        for child in familyList[fam].children: 
            if checkBirthBeforeMarriageOfParents_us08(family,individualList[child]) is not True:
                errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,child])
            if checkBirthNotAfter9MonthsDivorce_us08(family,individualList[child]) is not True:
                errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,child])

         # User Story 39
        if List_upcoming_anniversries_US39(family) is not True:
            for location in outputValues.location:
                errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,location])
            
    if List_orphans_US33(individualList, familyList) is not True:
            for location in outputValues.location:
                errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,location])

    

    writeTableToFile(errorTable,"Sprint4")


######################################################################################################################################################################
def List_upcoming_anniversries_US39(familyList):
    global outputValues
    outputValues = OutputValues("INFORMATION", "FAMILY", "US39","Upcoming anniversaries in next 30 days ")
    outputValues.location = []
    
    if familyList.marriage != 'NA':
        marriagedate = familyList.marriage
        today = date.today().strftime("%m-%d")
        
        dateB = datetime.strptime(marriagedate, "%Y-%m-%d")
        dateT = datetime.strptime(today, "%m-%d")
        
        if (dateB.date().year>=1900):
            marriage = datetime.strptime(dateB.strftime("%m-%d"),"%m-%d")
            recent_marriage =  marriage - dateT
            if(recent_marriage <= timedelta(days=30) and recent_marriage > timedelta(days=0)) or (recent_marriage <=timedelta(days=365) and recent_marriage > timedelta(days=335)):
                outputValues.location.append(familyList.ID)
                return False

######################################################################################################################################################################
def list_multipe_births_US32(individualList,individual):
    global outputValues
    outputValues = OutputValues("ERROR", "INDIVIDUAL", "US32", "Multiple births")
    outputValues.location = []

    for i in individualList:
        individual_id = individual.ID
        indi = individualList[i].ID   
        
        if individual_id != indi:
            birth = individual.birthday
            comp = individualList[i].birthday
            if(str(birth) == str(comp)):
                outputValues.location.append(individual_id)
                return False 

######################################################################################################################################################################
def correspondingEntries_us26(family, individualList):
	global outputValues
	error = False
	outputValues = OutputValues("ERROR", "FAM/INDI", "US26", "Corresponding Entries do not match")
	outputValues.location = []
	husband = family.husband
	wife = family.wife
	if (family.ID != individualList[husband].spouseFamily):
		error = True
		outputValues.location.append(family.ID + "-" + husband)
	if (family.ID != individualList[wife].spouseFamily):
		error = True
		outputValues.location.append(family.ID + "-" + wife)
	for child in family.children:
		if (family.ID != individualList[child].childFamily):
			error = True
			outputValues.location.append(family.ID + "-" + child)
	return error

######################################################################################################################################################################
def orderSiblings_us28(family, individualList):
	global outputValues
	outputValues = OutputValues("INFORMATION", "FAMILY", "US28", "Ordered Siblings")
	outputValues.location = "No children"
	if (family.children):
		outputValues.location = family.ID
		children = family.children
		for i in xrange(len(children)-1):
			j = i+1
			if (individualList[children[i]].age <= individualList[children[j]].age):
				temp = children[i]
				children[i] = children[j]
				children[j] = temp
		for child in children:
			outputValues.location = outputValues.location +  " " + child
		return outputValues.location

######################################################################################################################################################################

def checkDivorceBeforeDeath_us06(family,individual):
    global outputValues
    outputValues=OutputValues("ERROR","family","US06","divorce "+ family.divorce+" is after death "+individual.death+" of individual ")
    if family.marriage=='NA':
        outputValues.description="marriage date not specified"
        return False
    if individual.birthday=='NA':
        outputValues.description="birth date not specified"
        return False
    if individual.death=='NA':
        return True
    if family.divorce=='NA':
        return True
    return checkDate( family.divorce, individual.death)

######################################################################################################################################################################
        
def checkBirthBeforeMarriageOfParents_us08(family,individual):
    global outputValues
    outputValues=OutputValues("ERROR","family","US08","birth of child "+ individual.birthday+" is before marriage "+family.marriage+" of parents ")
    if family.marriage=='NA':
        outputValues.description="marriage date not specified"
        return False
    if individual.birthday=='NA':
        outputValues.description="birth date not specified"
        return False
    return checkDate( family.marriage, individual.birthday)

######################################################################################################################################################################

def checkBirthNotAfter9MonthsDivorce_us08(family,individual):
    global outputValues
    outputValues=OutputValues("ERROR","family","US08","birth of child "+ individual.birthday+" is after nine months of divorce "+family.divorce+" of parents ")
    if family.marriage=='NA':
        outputValues.description="marriage date not specified"
        return False
    if individual.birthday=='NA':
        outputValues.description="birth date not specified"
        return False
    if family.divorce=='NA':
        return True
    if checkDate(individual.birthday,family.divorce) is True:
        return True
    return dates_within(family.divorce, individual.birthday, 9, 'months')


######################################################################################################################################################################
def List_upcoming_birthdsy_US38(individualList):
    global outputValues
    outputValues = OutputValues("INFORMATION", "INDIVIDUAL", "US38","List_upcoming_birthdays")
    outputValues.location = []
    
    if individualList.birthday != 'NA':
        birthdate = individualList.birthday
        today = date.today().strftime("%m-%d")
        
        dateB = datetime.strptime(birthdate, "%Y-%m-%d")
        dateT = datetime.strptime(today, "%m-%d")
        
        if (dateB.date().year>=1900):
            birth = datetime.strptime(dateB.strftime("%m-%d"),"%m-%d")
            recent_birth =  birth - dateT
            if(recent_birth <= timedelta(days=30) and recent_birth > timedelta(days=0)) or (recent_birth <=timedelta(days=365) and recent_birth > timedelta(days=335)):
                outputValues.location.append(individualList.ID)
                return False
#########################################################################################################################################################################

def List_orphans_US33(individualList, familyList):
    global outputValues
    outputValues = OutputValues("INFORMATION", "INDIVIDUAL", "US33"," List of Orphans ")
    outputValues.location = []
    for x in familyList:
            father_id = familyList[x].husband
            mother_id = familyList[x].wife
            child_type_check = familyList[x].children
            #print child_type_check
            father_death_date = None
            mother_death_date = None
            if type(child_type_check) is None:                                              
                pass
            elif(type(child_type_check) is list):
                 for z in range(len(child_type_check)):
                    current_child_id = child_type_check[z]
                    for i in individualList:
                        if(individualList[i].ID == father_id):
                            father_death_date = individualList[i].death
                        if(individualList[i].ID == mother_id):
                            mother_death_date = individualList[i].death
                        if(individualList[i].ID == current_child_id):
                            
                            child_id = individualList[i].ID
                            child_age = individualList[i].age
                            
                            if child_age < 18 and child_age > 0:
                                
                                if(mother_death_date != 'NA') and (father_death_date!= 'NA'):
                                    outputValues.location.append(child_id)

                                    
            else:
                for i in individualList:
                    if(individualList[i].ID == father_id):                                   
                        father_death_date = individualList[i].death
                    if(individualList[i].ID== mother_id):
                        mother_death_date = individualList[i].death
                    if(individualList[i].ID == child_type_check):
                        child_id1 = individualList[i].ID
                        child_age1 = individualList[i].age   
                        if child_age1 < 18 and child_age > 0:
                            if(father_death_date != 'NA') and (mother_death_date!= 'NA'):
                                outputValues.location.append(child_id1)                     
                                            
    return False                         
            
