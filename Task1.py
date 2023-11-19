import pandas
import os

courses=[]
hours={'hour1':'9-10','hour2':'10-11','hour3':'11-12','hour4':'12-1','hour5':'1-2','hour6':'2-3','hour7':'3-4','hour8':'4-5',}
count=0
coursestat={}
week=['None','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
response=0
done=0
global current
global choice
global title

class Course:
	sects=['',[],[],[]]
	
	def __init__(self, name,Mid_sem, Compre,Expla, Lec, Tut, Lab):
		self.name=name
		self.Mid_sem=Mid_sem
		self.Compre=Compre
		self.Expla=Expla
		self.Lec=Lec
		self.Tut=Tut
		self.Lab=Lab
		
	def __str__ (self):
		return 'Name:{} \n{} \n Exam Dates: Compre: {} Midsem: {}\nLec there:{} \nTut there: {}\nLab there: {}'.format(self.name, self.Expla, self.Compre, self.Mid_sem, self.Lec, self.Tut, self.Lab)
	
	def get_all_sections(self):
		if courses[current].Lec:
			print('Lecture sections are:')
			for value in self.sects[1]:
				print(value)
		if courses[current].Tut:
			print('Tutorial sections are:')
			for value in self.sects[2]:
				print(value)
		if courses[current].Lab:
			print('Lab sections are:')
			for value in self.sects[3]:
				print(value)
	
	def populate_section(self, typee):
		filename=input('Save file in user files and enter its name here')
		for file in os.listdir("./Userfiles"):
			if file==filename:
				df = pandas.read_csv(os.path.join('Userfiles',file), index_col=False)
				data = df.values.tolist()
				for p in data:
					self.sects[typee].append(Section(*p))


class Section:
	type=['none', 'Lecture', 'Tutotial','Lab' ]
	def __init__(self, sect, instructor, days, time):
		self.sect=sect
		self.instructor=instructor
		self.time=hours[time]
		self.days=days
	
	def __str__(self):
		return 'Section: {} Instructor: {} Days: {} Time:{}'.format(self.sect, self.instructor, self.days, self.time)
	
	def sectionnum(section):
		num=int(section[1:])-1
		return num


class Timetable:

	Table={'Monday':{'8-9':-1,'9-10':-1,'10-11':-1,'11-12':-1,'12-1':-1,'1-2':-1,'2-3':-1,'3-4':-1,'4-5':-1},
		'Tuesday':{'8-9':-1,'9-10':-1,'10-11':-1,'11-12':-1,'12-1':-1,'1-2':-1,'2-3':-1,'3-4':-1,'4-5':-1},
		'Wednesday':{'8-9':-1,'9-10':-1,'10-11':-1,'11-12':-1,'12-1':-1,'1-2':-1,'2-3':-1,'3-4':-1,'4-5':-1},
		'Thursday':{'8-9':-1,'9-10':-1,'10-11':-1,'11-12':-1,'12-1':-1,'1-2':-1,'2-3':-1,'3-4':-1,'4-5':-1},
		'Friday':{'8-9':-1,'9-10':-1,'10-11':-1,'11-12':-1,'12-1':-1,'1-2':-1,'2-3':-1,'3-4':-1,'4-5':-1},
		'Saturday':{'8-9':-1,'9-10':-1,'10-11':-1,'11-12':-1,'12-1':-1,'1-2':-1,'2-3':-1,'3-4':-1,'4-5':-1}}

	@classmethod	
	def enroll_subject(cls, ):
		response=input('Save file in user files and enter name of the file')
		subprocess.run(['cp',str(os.path.join('user files',response)),'Excel files'])
	
	@classmethod
	def period_removal(cls, naam):
		if naam[:2]=='Le':
			remtype=1
		else :
			if naam[:2]=='Tu':
				remtype=2
			else:
				remtype=3
		for value in coursestat.keys():
			if value in naam:
				remsub=value
				break
		day=[]
		position=0
		pos=len(naam)-1
		while True:
			try:
				int(naam[pos])
			except ValueError:
				break
			pos=pos-1

		choice=courses[coursestat[remsub][0]].sects[remtype][int(naam[pos+1:])-1]
		while position<len(choice.days):
			day.append(week[int(choice.days[position])])
			position+=2
		for value in day:
			Timetable.Table[value][choice.time]=-1
		if coursestat[remsub][1]==True and coursestat[remsub][2]==True and coursestat[remsub][3]==True:
			coursestat[remsub][remtype]=False
			return -1
		else:
			coursestat[remsub][remtype]=False
			return 0
	
	@classmethod
	def check_clashes(cls, typenum, current, choice, title, currsect):
		happy='yes'
		day=[]
		position=0
		while position<len(choice.days):
			day.append(week[int(choice.days[position])])
			position+=2
		stat=0
		for value in day:
			if Timetable.Table[value][choice.time]!=-1:
				happy='no'
				stat=stat+Timetable.period_removal(Timetable.Table[value][choice.time])

		if happy=='no':
			print('There were clashes, clashing slots emptied, current section not alloted')
			return -1+stat

		else:
			for value in day:
				Timetable.Table[value][choice.time]='{} {} {}'.format(Section.type[typenum], courses[current].name, currsect)
			print('Slots alloted')
			coursestat[title][typenum]=True
			if coursestat[title][1]==True and coursestat[title][2]==True and coursestat[title][3]==True:
				return 1
			else:
				return 0

	@classmethod
	def export_to_csv(cls):
		pandas.DataFrame(cls.Table).to_csv('Timetable.csv', index=True)



key=input("Please enter password, leave empty if no password")
if key =='1234':
	response=input("You want to add an excel files? (enter 'Yes' if you want to)")
	if response=='Yes':
		Timetable.enroll_subject()
	
	

for file in os.listdir("./Excel files"):
	if file.endswith('.xlsx'):
		df = pandas.read_excel(os.path.join('Excel files',file), sheet_name='Data') 
		data = df.values.tolist()
		for p in data:
			courses.append(Course(*p))
		if courses[count].Lec:
			df = pandas.read_excel(os.path.join('Excel files',file), sheet_name='Lect') 
			data = df.values.tolist()
			for p in data:
				courses[count].sects[1].append(Section(*p))
		if courses[count].Tut:
			df = pandas.read_excel(os.path.join('Excel files',file), sheet_name='Tut') 
			data = df.values.tolist()
			for p in data:
				courses[count].sects[2].append(Section(*p))
		if courses[count].Lab:
			df = pandas.read_excel(os.path.join('Excel files',file), sheet_name='Lab') 
			data = df.values.tolist()
			for p in data:
				courses[count].sects[3].append(Section(*p))
		#counter= counter+int(courses[count].Lab)+int(courses[count].Tut)+int(courses[count].Lec)
		count=count+1

response='Yes'
if key=='1234':
	while (response=='Yes'):
		response=input("You want to add sections? (keep entering 'Yes' to this message if you want to)")
		if response=='Yes':
			Sub=input('Enter subject')
			typee=input('Write 1 for Lecture, 2 for Tutorial and 3 for Lab')
			courses[coursestat[Sub][0]].populate_section(typee)

response=0

print("Hello there, let us make your time table")
print("The courses are:")



for i in range(count):
	print(courses[i].name)
	coursestat[courses[i].name]=[i,True,True, True]
	if courses[i].Lec: 
		coursestat[courses[i].name][1]=False
	if courses[i].Tut: 
		coursestat[courses[i].name][2]=False
	if courses[i].Lab: 
		coursestat[courses[i].name][3]=False

print("Type 'QUIT' to quit")

while(response!='QUIT' and done!=count):
	response=input("For which course you want to select the sections")
	
	
	if response in coursestat.keys():
		
		current=coursestat[response][0]
		title=response
		print(courses[current])
		
		courses[current].get_all_sections()
		print('{}{}{}'.format('Enter 1 to enter Lecture section\n' if not coursestat[response][1] else '','Enter 2 to enter Tutorial section\n' if not coursestat[response][2] else '','Enter 3 to enter Lab section\n' if not coursestat[response][3] else ''))
		if '{}{}{}'.format('Enter 1 to enter Lecture section\n' if not coursestat[response][1] else '','Enter 2 to enter Tutorial section\n' if not coursestat[response][2] else '','Enter 3 to enter Lab section\n' if not coursestat[response][3] else '')=='':
			print('This course sections have been selected.')
			continue
		else:	
			x=int(input())
		
		if x<4:
			typenum=x
		else:
			print('Enter correct number')
			continue
		
		if not coursestat[title][typenum]:
			response=input("Which section you choose?")
			currsect=response
			choice=courses[current].sects[typenum][Section.sectionnum(response)]
			done=done+Timetable.check_clashes(typenum, current, choice, title, currsect)
		else:
			print("Slot for {} is already set".format(Section.type[typenum]))

		'''	
		if courses[current].Lab and response=='Lab':
			print('Sections are:')
			courses[current].labdisplay()
			response=input("Which section you choose?")
			choice=Section.sectionnum(response)
			if courses[current].sects[3][choice].clash('Lab')=="Yes":
				print("Sorry this time slot clashes, we have reset clashing time intervals")
			else:
				done+=1
				print("The slot was set")
					
		
		if courses[current].Tut and response=='Tut':
			success=0
			print('Sections are:')
			courses[current].tutdisplay()
			response=input("Which section you choose?")
			choice=Section.sectionnum(response)
			if courses[current].sects[2][choice].clash('Tut')=="Yes":
				print("Sorry this time slot clashes, we have reset clashing time intervals")
			else:
				print("The slot was set")
				done+=1
				print (count,done)
		'''


	else:
		print("The value is wrong")
	not_done=''
	for value in coursestat.keys():
		if coursestat[value][1]==False or coursestat[value][2]==False or coursestat[value][3]==False:
			not_done=not_done[:]+' '+value
	if not_done=='':
		print('All subjects entered')
	else:
		print(not_done,' is(are) yet to be filled')
		response=input("type 'QUIT' to quit, press enter to continue")

Timetable.export_to_csv()
print('Timetable was made')