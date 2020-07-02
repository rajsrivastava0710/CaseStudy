#*******************************************************************************#

# Imports

from flask import redirect, url_for, Response, session, render_template, request, flash
from application import app, mysql
from application.form import SearchDiagnosticsForm, SearchMedicinesForm, LoginForm, CreatePatientForm, DeletePatientForm, UpdatePatientForm, SearchPatientForm
from application.middlewares import is_logged_in, is_not_logged_in
from datetime import datetime

#-------------------------------------------------------------------------------#

#Index Route

# Welcome Page

@app.route('/')
def index():
	return render_template('home.html')

#-------------------------------------------------------------------------------#

# login for Admin

#Login only for admin(Id:admin@tcs.com,Pass:tcs_knit)

@app.route('/login',methods=['GET','POST'])
@is_not_logged_in
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		
		# checking if credentials are correct 

		curr = mysql.connection.cursor()
		result = curr.execute("SELECT * FROM userstore WHERE login = %s",[username])

		#Correct

		if(result>0):
			data = curr.fetchone()
			if password == data['password']:
				session['logged_in'] = True
				session['username'] = username
				session['name'] = 'Admin'
				flash('Logged in successfully', 'success')
				return redirect(url_for('index'))
			else:
				flash('Invalid Username/Password','danger')
			curr.close()

		# Incorrect

		else:
			flash('Invalid Username/Password','danger')

		return redirect(url_for('login'))	
	else:
		form = LoginForm()
		return render_template('login.html', form = form)


#-------------------------------------------------------------------------------#

#Logout for admin

@app.route('/logout')
@is_logged_in
def logout():

	# clear the session

    session.clear()
    flash('Logged out successfully !','success')
    return redirect(url_for('login'))

#-------------------------------------------------------------------------------#
# Patients
#______________________________________________________________________________#

#CREATE page
@app.route('/create_patient', methods = ['GET', 'POST'])
@is_logged_in
def create_patient():
	form = CreatePatientForm()
	
	#Get Max SSNId and PatientId from database
	cur = mysql.connection.cursor()
	res = cur.execute("SELECT MAX(`patientId`) as maxId, MAX(`patientSsnID`) as maxSsnId from patients")
	maxi = cur.fetchone()
	maxId = maxi['maxId']
	maxSsnId = maxi['maxSsnId']
	cur.close()

	#Incrementing the ids for new patient(for auto ids on frontend)
	if maxId:
		maxId= int(maxId)+1
	else:
		maxId = 100000001
	if maxSsnId:
		maxSsnId = int(maxSsnId)+3
	else:
		maxSsnId = 101324032

	# Post Request
	if request.method == 'POST':
		patientSsnId = form.patientSSNID.data
		patientName = form.patientName.data.strip()
		age = form.patientAge.data
		dateOfAdmission = form.dateOfAdmission.data
		address = form.address.data.strip()
		state = form.state.data.strip()
		city = form.city.data.strip()
		typeOfBed = form.typeOfBed.data
		status = 'Occupied'

		#Name validation for only alphabets
		name_array = patientName.split(' ')
		for name in name_array:
			if not name.isalpha():
				flash('Patient creation failed!! Name can only only contain Alphabets!','danger')
				return redirect(url_for('create_patient'))
			
		#Age validation
		if str(age).isalpha() or age/999>1:
			flash('Patient creation failed!! Invalid Age!','danger')
			return redirect(url_for('create_patient'))

		#SSN ID validation
		check = patientSsnId / 100000000
		if check <= 1:
			flash('SSN ID must be of 9 digits','danger')
			return redirect(url_for('create_patient'))

		#Check if patient with same ssnid already exists
		cur = mysql.connection.cursor()
		result = cur.execute("SELECT * from patients WHERE patientSsnId = %s",[patientSsnId])
		cur.close()

		# if no duplicates exist
		if result == 0 :
			#create entry of patient in table
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO patients(patientSsnId,patientId,patientName,age,dateOfAdmission,address,state,city,typeOfBed,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(patientSsnId,maxId,patientName,age,dateOfAdmission,address,state,city,typeOfBed,status))
			mysql.connection.commit()
			cur.close()
			flash('Patient created successfully!','success')
			return redirect(url_for('view_patient'))

		#if duplicate exist, give error message
		else:
			flash('Patient with this SSN ID already exists','danger')
			return redirect(url_for('create_patient'))

	#Auto Suggesting SSN ID
	form.patientSSNID.data = maxSsnId

	return render_template('create_patient.html', form = form)


#-------------------------------------------------------------------------------#


#READ Page

@app.route('/view_patient', methods = ['GET', 'POST'])
@is_logged_in
def view_patient():

	# get all patient 

	cur = mysql.connection.cursor()
	cur.execute("select * from patients")
	data=cur.fetchall()
	
	return render_template('view_patient.html', data = data)


#-------------------------------------------------------------------------------#


#DELETE PAGE

@app.route('/delete_patient', methods = ['GET', 'POST'])
@is_logged_in
def get_delete_patient():
	form = DeletePatientForm()
	if request.method == 'POST':
		data = form.patientID.data

		#Check if patient with the id exists

		cur = mysql.connection.cursor()
		result = cur.execute("select * from patients where patientId=%s",[data])
		patient = cur.fetchone()
		cur.close()

		# if exists
		if(result > 0):
			flash('Patient found','success')
			return render_template('delete_patient.html',form=form,patient=patient)
		
		# if doesnt exist, give error message
		else:
			flash('Patient does not exist','danger')
			return redirect(url_for('get_delete_patient'))

	return render_template('delete_patient.html', form = form)


#-------------------------------------------------------------------------------#


#DELETE ROUTE

@app.route('/patient/<string:id>/destroy',methods=['GET','POST'])
@is_logged_in
def destroy_patient(id):
	if request.method == 'POST':

		# delete patient's data from table 
		
		cur = mysql.connection.cursor()
		result = cur.execute("delete from patients where patientId=%s",[id])
		mysql.connection.commit()
		cur.close()
		
		if(result > 0):
			flash('Patient deleted successfully!','success')
			return redirect(url_for('view_patient'))
		else:
			flash('User does not exist','danger')
			return redirect(url_for('get_delete_patient'))
	
	return redirect(url_for('get_delete_patient'))


#-------------------------------------------------------------------------------#


# Update Page

@app.route('/update_patient', methods = ['GET', 'POST'])
@is_logged_in
def update_patient():
	form = UpdatePatientForm()
	if request.method == 'POST':
		data = form.patientID.data
		# pass patient id to update as query params
		return redirect(url_for('create_patient_update', dataupdate = data))
	return render_template('update_patient.html', form = form)


#-------------------------------------------------------------------------------#


# Update Route

@app.route('/create_patient_update', methods = ['GET', 'POST'])
@is_logged_in
def create_patient_update():

	# get query params
	_id = request.args.get('dataupdate')
	
	#search patient from id
	cur = mysql.connection.cursor()
	result = cur.execute("select *from patients where patientId=%s",[_id])
	patient = cur.fetchone()
	cur.close()

	form = CreatePatientForm()
	
	if request.method == "POST":
		# if patient with the id exist
		if result > 0:
			patientName = form.patientName.data.strip()
			age = form.patientAge.data
			address = form.address.data.strip()
			dateOfAdmission = form.dateOfAdmission.data
			typeOfBed = form.typeOfBed.data
			city = form.city.data.strip()
			state = form.state.data.strip()

			# Name Validation
			name_array = patientName.split(' ')
			for name in name_array:
				if not name.isalpha():
					flash('Patient Updation failed!! Name can only only contain Alphabets!','danger')
					return redirect(url_for('create_patient_update',dataupdate = _id))
			
			# Age Validation				
			if str(age).isalpha() or age/999>1:
				flash('Patient updation failed!! Invalid Age!','danger')
				return redirect(url_for('create_patient_update', dataupdate = _id))

			# Query for updation
			curr = mysql.connection.cursor()
			curr.execute("UPDATE patients SET patientName=%s, age=%s, address=%s, dateOfAdmission=%s, typeOfBed=%s, city=%s, state=%s WHERE patientId=%s",(patientName,age,address,dateOfAdmission,typeOfBed,city,state,_id))
			mysql.connection.commit()
			curr.close()

			flash('Patient details have been updated!','success')

			return redirect(url_for('view_patient'))

		# if patient with the id does not exist	
		else:
			flash('No such Patient found','danger')
			return redirect(url_for('update_patient'))

	# Prefilling of previous values in inputs for get req
	if result>0:
		form.patientName.data = patient['patientName']
		form.patientAge.data = patient['age']
		form.address.data = patient['address']
		form.dateOfAdmission.data = patient['dateOfAdmission']
		form.typeOfBed.data = patient['typeOfBed']
		form.city.data = patient['city']
		form.state.data = patient['state']
		return render_template('update_patient_by_id.html', form = form,_id=_id)
	else:
		flash('No such Patient found','danger')
		return redirect(url_for('update_patient'))


#-------------------------------------------------------------------------------#


#search

@app.route('/search_patient', methods = ['GET', 'POST'])
@is_logged_in
def search_patient():
	form = SearchPatientForm()
	if request.method == 'POST':

		_id = form.patientID.data
		
		# Query to find patient from id
		cur = mysql.connection.cursor()
		result = cur.execute("select *from patients where patientId=%s",[_id])
		patient = cur.fetchone()
		cur.close()
		
		if result>0:
			flash('Patient found','success')
			return render_template('search_patient_by_id.html', patient = patient)
		else:
			flash('No such user exists!','danger');
	return render_template('search_patient.html', form = form)

#-------------------------------------------------------------------------------#

#MEDICINES

#_______________________________________________________________________________#


#READ Page

@app.route('/medicines/all')
@is_logged_in
def all_medicines():

	# query for all medicines in db

	cur = mysql.connection.cursor()
	result = cur.execute("select * from medicinesmaster")
	medicines = cur.fetchall()

	return render_template('all_medicines.html',medicines=medicines)

#-------------------------------------------------------------------------------#


# Search via patient id

@app.route('/patient/medicines',methods=['GET','POST'])
@is_logged_in
def get_patient_medicine():

	form = SearchPatientForm()
	
	if request.method == 'POST':
		_id = form.patientID.data
		
		# get patient by id

		cur = mysql.connection.cursor()
		result = cur.execute("select *from patients where patientId=%s",[_id])
		patient = cur.fetchone()
		cur.close()

		if result>0:
			# passing patient id 
			return redirect(url_for('medicines_section',id=_id))
		else:
			flash('No such user exists!','danger');

	return render_template('search_patient_medicine.html',form=form)


#-------------------------------------------------------------------------------#


# pharmacy detail of patient

@app.route('/patient/<string:id>/medicines',methods=['GET'])
@is_logged_in
def medicines_section(id):

	# find patient by id

	cur = mysql.connection.cursor()
	result = cur.execute("select * from patients where patientId=%s",[id])
	patient = cur.fetchone()
	cur.close()

	# find medicines issued to the patient

	curr = mysql.connection.cursor()
	result = curr.execute("select medicinesmaster.medicineName, medicinesmaster.rateOfMedicine,medicinepatient.quantityIssued from medicinepatient inner join medicinesmaster on medicinepatient.medicineId=medicinesmaster.medicineId where patientId=%s",[id])
	medicines = curr.fetchall()
	curr.close()

	return render_template('medicines_dashboard.html',patient=patient,medicines=medicines)

#-------------------------------------------------------------------------------#

# search for medicine via id

@app.route('/patient/<string:id>/medicines/add',methods=['GET','POST'])
@is_logged_in
def add_medicines(id):
	form = SearchMedicinesForm()
	if request.method == 'POST':

		#query to find medicine by name

		medicineName = form.medicineName.data+'%'
		cur = mysql.connection.cursor()
		result = cur.execute("select * from medicinesmaster where LCASE(medicinesmaster.`medicineName`) LIKE %s",[medicineName])
		medicine = cur.fetchone()
		cur.close()

		# medicine Available 
		if result>0 and medicine['quantityAvailable']>0 :
			flash('Available in stock','success')
		# medicine does not exist with the name
		elif result<=0 :
			flash('Medicine does not exist with this name','danger')
		# medicine not in stock
		else:
			flash('Not Available in Stock','danger')
		
		return render_template('add_medicines.html',form=form,medicine = medicine,id=id)
	
	return render_template('add_medicines.html',form=form)


#-------------------------------------------------------------------------------#


# Issue a medicine to patient

@app.route('/addMedicine/<string:mId>/patient/<string:pId>',methods=['POST'])
@is_logged_in
def addMedicineToPatient(mId,pId):

	# quantity of medicine we want to issue
	quantity = int(request.form['quantity'])

	# query to get patient
	cur = mysql.connection.cursor()
	res = cur.execute('select * from patients where patientId = %s',[pId])
	patient = cur.fetchone()
	cur.close()

	# get details of medicines issued by the patient
	cur = mysql.connection.cursor()
	res = cur.execute("select * from medicinesmaster where medicineId = %s",[mId])
	medicine = cur.fetchone()
	cur.close()

	# allow only if issued medicine < total available medicine
	# and patient yet not discharged

	if int(medicine['quantityAvailable'])>=int(quantity) and patient['status'] != 'Discharged':
		
		# update medicine master table to reduce available medicine quantity

		curr=mysql.connection.cursor()
		result = curr.execute("update medicinesmaster set quantityAvailable = quantityAvailable - %s where medicineId=%s",(quantity,mId))
		mysql.connection.commit()
		curr.close()
		
		# insert new entry of patient with medicine in table

		cur =  mysql.connection.cursor()
		res = cur.execute("insert into medicinepatient(patientId,medicineId,quantityIssued) values(%s, %s, %s)",(pId,mId,quantity))
		cur.connection.commit();
		cur.close()
		flash('Medicine issued successfully','success')

	# not allow if patient is discharged
	elif patient['status'] == 'Discharged':
		flash('Patient already discharged. Can not add medicine!','danger')

	#not allow if quantity issued exceeds quanatity available
	else:
		flash('Quantity Exceeded, Medicine Issue failed!','danger')

	return redirect(url_for('medicines_section',id=pId))


#-------------------------------------------------------------------------------#


#DIAGNOSTICS

# _____________________________________________________________________________#


# Read

@app.route('/diagnostics/all')
@is_logged_in
def all_diagnostics():
	
	# FInd all diagnostics
	cur = mysql.connection.cursor()
	result = cur.execute("select * from diagnosticsmaster")
	diagnostics = cur.fetchall()

	return render_template('all_diagnostics.html',diagnostics=diagnostics)


#-------------------------------------------------------------------------------#


#search via patient id

@app.route('/patient/diagnostics',methods=['GET','POST'])
@is_logged_in
def get_patient_diagnostics():

	form = SearchPatientForm()
	
	if request.method == 'POST':
		# find patient via id
		_id = form.patientID.data
		cur = mysql.connection.cursor()
		result = cur.execute("select * from patients where patientId=%s",[_id])
		patient = cur.fetchone()
		cur.close()

		if result>0:
			return redirect(url_for('diagnostics_section',id=_id))	
		else:
			flash('No such patient exists!','danger');

	return render_template('search_patient_diagnostic.html',form=form)


#-------------------------------------------------------------------------------#

# diagnostic page of patient

@app.route('/patient/<string:id>/diagnostics',methods=['GET','POST'])
@is_logged_in
def diagnostics_section(id):

	# find patient via id

	cur = mysql.connection.cursor()
	result = cur.execute("select * from patients where patientId=%s",[id])
	patient = cur.fetchone()
	cur.close()

	#find details of diagnostics of patient
	curr = mysql.connection.cursor()
	result = curr.execute("select diagnosticsmaster.testName, diagnosticsmaster.testCharge from diagnosticpatient inner join diagnosticsmaster on diagnosticpatient.testId=diagnosticsmaster.testId where patientId=%s",[id])
	diagnostics = curr.fetchall()

	return render_template('diagnostics_dashboard.html',patient=patient,diagnostics = diagnostics)


#-------------------------------------------------------------------------------#

# search test via id

@app.route('/patient/<string:id>/diagnostics/add',methods=['GET','POST'])
@is_logged_in
def add_diagnostics(id):

	form = SearchDiagnosticsForm()
	
	if request.method == 'POST':
		
		# search by test name

		testName = form.testName.data + '%'
		cur = mysql.connection.cursor()
		result = cur.execute("select * from diagnosticsmaster where LCASE(diagnosticsmaster.`testName`) LIKE %s",[testName])
		diagnostic = cur.fetchone()
		cur.close()
		
		if result>0 :
			flash('Test Available','success')
		else :
			flash('Test does not exist with this Name','danger')
		
		return render_template('add_diagnostics.html',form=form,diagnostic = diagnostic,id=id)
	
	return render_template('add_diagnostics.html',form=form)


#-------------------------------------------------------------------------------#


# issue test to patient page

@app.route('/addDiagnostic/<string:dId>/patient/<string:pId>',methods=['POST'])
@is_logged_in
def add_diagnostic_to_patient(dId,pId):

	# find patient by id

	cur = mysql.connection.cursor()
	res = cur.execute('select * from patients where patientId = %s',[pId])
	patient = cur.fetchone()
	cur.close()

	# issue test only if patient is not discharged

	if patient['status'] == 'Discharged':
		flash('Patient is already discharged. Could not add the test!','danger')

	else:

		# insert data of patient issuing test in table

		cur =  mysql.connection.cursor()
		res = cur.execute("insert into diagnosticpatient(patientId,testId) values(%s, %s)",(pId,dId))
		cur.connection.commit();
		cur.close()
		flash('Test issued successfully','success')
		

	return redirect(url_for('diagnostics_section',id=pId))


#-------------------------------------------------------------------------------#

#BILLING SETION

# billing page and payment confirmation

@app.route('/patient/<string:pId>/billing',methods=['GET','POST'])
@is_logged_in
def billing_screen(pId):
	if request.method == 'POST':
		# date of discharge is the current time
		dod = datetime.now()
		
		#quert to update date of discharge in patients table
		cur =mysql.connection.cursor()
		result = cur.execute('update patients set status = %s, dateOfDischarge = %s where patientId = %s',('Discharged',dod,pId))
		mysql.connection.commit()
		cur.close()
		
		flash('Billing Confirmation done','success')
		return redirect(url_for('billing_screen',pId=pId))
	
	else:

		#get patient details	
		
		cur = mysql.connection.cursor()
		res = cur.execute("select * from patients where patientId = %s",[pId])
		patient = cur.fetchone()
		cur.close()
		
		#Get the number of days from difference between doa and dod

		if patient['dateOfDischarge']:
			current_time = patient['dateOfDischarge']
		else:
			current_time = datetime.now()

		#getting days from the string

		_array = str(current_time - patient['dateOfAdmission']).split(' ')
		
		#for discharge on same day , consider 1 day
		if len(_array)==1 :
			difference = 1
		#if doa is after dod , keep days as 0
		else :
			difference = int(0 if int(_array[0])<0 else int(_array[0]))

		#getting room fees
		if patient['typeOfBed'] == 'Single Room':
			roomFee = 8000*difference
		elif patient['typeOfBed'] == 'Semi Sharing':
			roomFee = 4000*difference
		else:
			roomFee = 2000*difference

		#get patient's diagnostics data

		curr = mysql.connection.cursor()
		result = curr.execute("select diagnosticsmaster.testName, diagnosticsmaster.testCharge from diagnosticpatient inner join diagnosticsmaster on diagnosticpatient.testId=diagnosticsmaster.testId where patientId=%s",[pId])
		diagnostics = curr.fetchall()
		curr.close()

		# get patients's diagnostics total charges

		curr = mysql.connection.cursor()
		result = curr.execute("select SUM(diagnosticsmaster.testCharge) as diagSum from diagnosticpatient inner join diagnosticsmaster on diagnosticpatient.testId=diagnosticsmaster.testId where patientId=%s",[pId])
		diagnosticTotal = curr.fetchone()
		curr.close()

		#get patient's pharmacy data

		currr = mysql.connection.cursor()
		result = currr.execute("select medicinesmaster.medicineName, medicinesmaster.rateOfMedicine,medicinepatient.quantityIssued from medicinepatient inner join medicinesmaster on medicinepatient.medicineId=medicinesmaster.medicineId where patientId=%s",[pId])
		medicines = currr.fetchall()
		currr.close()

		#get patient's pharmacy total charges

		currr = mysql.connection.cursor()
		result = currr.execute("select SUM(medicinesmaster.rateOfMedicine * medicinepatient.quantityIssued) as medSum from medicinepatient inner join medicinesmaster on medicinepatient.medicineId=medicinesmaster.medicineId where patientId=%s",[pId])
		medicineTotal = currr.fetchone()
		currr.close()

		#if no pharmacy or diagnostic records exist , make the total 0 to avoid Nan

		if medicineTotal['medSum'] == None:
			medicineTotal['medSum'] = 0
		if diagnosticTotal['diagSum'] == None:
			diagnosticTotal['diagSum'] = 0

		return render_template('billing.html',patient=patient,difference=difference,roomFee=roomFee,medicines = medicines, diagnostics = diagnostics,medicineTotal=medicineTotal['medSum'],diagnosticTotal=diagnosticTotal['diagSum'])

#********************************************************************************#
