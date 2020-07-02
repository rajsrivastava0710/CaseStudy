from flask import redirect, url_for, Response, session, render_template, request, flash
from application import app, mysql
from application.form import SearchDiagnosticsForm, SearchMedicinesForm, LoginForm, CreatePatientForm, DeletePatientForm, UpdatePatientForm, SearchPatientForm
from application.middlewares import is_logged_in, is_not_logged_in
from datetime import datetime

#Index Route

@app.route('/')
def index():
	return render_template('home.html')

# login for Admin

@app.route('/login',methods=['GET','POST'])
@is_not_logged_in
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		curr = mysql.connection.cursor()
		result = curr.execute("SELECT * FROM userstore WHERE login = %s",[username])

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
		else:
			flash('Invalid Username/Password','danger')

		return redirect(url_for('login'))	
	else:
		form = LoginForm()
		return render_template('login.html', form = form)

#Logout for admin

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('Logged out successfully !','success')
    return redirect(url_for('login'))

# Patients

#CREATE page
@app.route('/create_patient', methods = ['GET', 'POST'])
@is_logged_in
def create_patient():
	form = CreatePatientForm()
	if request.method == 'POST':
		patientSsnId = form.patientSSNID.data
		patientName = form.patientName.data
		age = form.patientAge.data
		dateOfAdmission = form.dateOfAdmission.data
		address = form.address.data
		state = form.state.data
		city = form.city.data
		typeOfBed = form.typeOfBed.data
		status = 'Occupied'

		if not patientName.isalpha():
			flash('Patient creation failed!! Name can only only contain Alphabets!','danger')
			return redirect(url_for('create_patient'))

		check = patientSsnId / 100000000
		if check <= 1:
			flash('SSN ID must be of 9 digits','danger')
			return redirect(url_for('create_patient'))

		cur = mysql.connection.cursor()
		res = cur.execute("SELECT MAX(`patientId`) as maxId from patients")
		maxi = cur.fetchone()
		maxId = (maxi['maxId'])
		cur.close()
		if maxId:
			maxId= int(maxId)+1
		else:
			maxId = 100000001

		cur = mysql.connection.cursor()
		result = cur.execute("SELECT * from patients WHERE patientSsnId = %s",[patientSsnId])
		cur.close()

		if result == 0 :
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO patients(patientSsnId,patientId,patientName,age,dateOfAdmission,address,state,city,typeOfBed,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(patientSsnId,maxId,patientName,age,dateOfAdmission,address,state,city,typeOfBed,status))
			mysql.connection.commit()
			cur.close()
			flash('Patient created successfully!','success')
			return redirect(url_for('view_patient'))
		else:
			flash('Patient with this Id already exists','danger')
			return redirect(url_for('create_patient'))
	return render_template('create_patient.html', form = form)

#READ Page

@app.route('/view_patient', methods = ['GET', 'POST'])
@is_logged_in
def view_patient():
	cur = mysql.connection.cursor()
	cur.execute("select * from patients")
	data=cur.fetchall()
	return render_template('view_patient.html', data = data)


#DELETE PAGE

@app.route('/delete_patient', methods = ['GET', 'POST'])
@is_logged_in
def get_delete_patient():
	form = DeletePatientForm()
	if request.method == 'POST':
		data = form.patientID.data
		cur = mysql.connection.cursor()
		result = cur.execute("select * from patients where patientId=%s",[data])
		patient = cur.fetchone()
		cur.close()
		if(result > 0):
			flash('Patient found','success')
			return render_template('delete_patient.html',form=form,patient=patient)
		else:
			flash('Patient does not exist','danger')
			return redirect(url_for('get_delete_patient'))
	return render_template('delete_patient.html', form = form)

#DELETE ROUTE

@app.route('/patient/<string:id>/destroy',methods=['GET','POST'])
@is_logged_in
def destroy_patient(id):
	if request.method == 'POST':
		data = id
		cur = mysql.connection.cursor()
		result = cur.execute("delete from patients where patientId=%s",[data])
		mysql.connection.commit()
		cur.close()
		if(result > 0):
			flash('Patient deleted successfully!','success')
			return redirect(url_for('view_patient'))
		else:
			flash('User does not exist','danger')
			return redirect(url_for('get_delete_patient'))
	return redirect(url_for('get_delete_patient'))

# Update Page

@app.route('/update_patient', methods = ['GET', 'POST'])
@is_logged_in
def update_patient():
	form = UpdatePatientForm()
	if request.method == 'POST':
		data = form.patientID.data
		return redirect(url_for('create_patient_update', dataupdate = data))
	return render_template('update_patient.html', form = form)

# Update Route

@app.route('/create_patient_update', methods = ['GET', 'POST'])
@is_logged_in
def create_patient_update():
	_id = request.args.get('dataupdate')
	cur = mysql.connection.cursor()
	result = cur.execute("select *from patients where patientId=%s",[_id])
	patient = cur.fetchone()
	cur.close()
	form = CreatePatientForm()
	if request.method == "POST":
		if result > 0:
			patientName = form.patientName.data
			age = form.patientAge.data
			address = form.address.data
			dateOfAdmission = form.dateOfAdmission.data
			typeOfBed = form.typeOfBed.data
			city = form.city.data
			state = form.state.data

			curr = mysql.connection.cursor()
			curr.execute("UPDATE patients SET patientName=%s, age=%s, address=%s, dateOfAdmission=%s, typeOfBed=%s, city=%s, state=%s WHERE patientId=%s",(patientName,age,address,dateOfAdmission,typeOfBed,city,state,_id))
			mysql.connection.commit()
			curr.close()

			flash('Patient details have been updated!','success')

			return redirect(url_for('view_patient'))

		else:
			flash('No such Patient found','danger')
			return redirect(url_for('update_patient'))

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

#search

@app.route('/search_patient', methods = ['GET', 'POST'])
@is_logged_in
def search_patient():
	form = SearchPatientForm()
	if request.method == 'POST':
		_id = form.patientID.data
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

#MEDICINES

#READ Page

@app.route('/medicines/all')
@is_logged_in
def all_medicines():
	cur = mysql.connection.cursor()
	result = cur.execute("select * from medicinesmaster")
	medicines = cur.fetchall()
	return render_template('all_medicines.html',medicines=medicines)

# Search via patient id

@app.route('/patient/medicines',methods=['GET','POST'])
@is_logged_in
def get_patient_medicine():
	form = SearchPatientForm()
	if request.method == 'POST':
		_id = form.patientID.data
		cur = mysql.connection.cursor()
		result = cur.execute("select *from patients where patientId=%s",[_id])
		patient = cur.fetchone()
		cur.close()
		if result>0:
			return redirect(url_for('medicines_section',id=_id))
			# return render_template('medicines_dashboard.html', patient = patient)
		else:
			flash('No such user exists!','danger');

	return render_template('search_patient_medicine.html',form=form)

# pharmacy detail of patient

@app.route('/patient/<string:id>/medicines',methods=['GET','POST'])
@is_logged_in
def medicines_section(id):
	cur = mysql.connection.cursor()
	result = cur.execute("select * from patients where patientId=%s",[id])
	patient = cur.fetchone()
	cur.close()
	curr = mysql.connection.cursor()
	result = curr.execute("select medicinesmaster.medicineName, medicinesmaster.rateOfMedicine,medicinepatient.quantityIssued from medicinepatient inner join medicinesmaster on medicinepatient.medicineId=medicinesmaster.medicineId where patientId=%s",[id])
	medicines = curr.fetchall()
	curr.close()
	return render_template('medicines_dashboard.html',patient=patient,medicines=medicines)

# search for medicine via id

@app.route('/patient/<string:id>/medicines/add',methods=['GET','POST'])
@is_logged_in
def add_medicines(id):
	form = SearchMedicinesForm()
	if request.method == 'POST':
		medicineName = form.medicineName.data+'%'
		cur = mysql.connection.cursor()
		result = cur.execute("select * from medicinesmaster where LCASE(medicinesmaster.`medicineName`) LIKE %s",[medicineName])
		medicine = cur.fetchone()
		cur.close()
		if result>0 and medicine['quantityAvailable']>0 :
			flash('Available in stock','success')
		elif result<=0 :
			flash('Medicine does not exist with this name','danger')
		else:
			flash('Not Available in Stock','danger')
		return render_template('add_medicines.html',form=form,medicine = medicine,id=id)
	return render_template('add_medicines.html',form=form)

# Issue a medicine to patient

@app.route('/addMedicine/<string:mId>/patient/<string:pId>',methods=['POST'])
@is_logged_in
def addMedicineToPatient(mId,pId):

	quantity = int(request.form['quantity'])

	cur = mysql.connection.cursor()
	res = cur.execute('select * from patients where patientId = %s',[pId])
	patient = cur.fetchone()
	cur.close()

	cur = mysql.connection.cursor()
	res = cur.execute("select * from medicinesmaster where medicineId = %s",[mId])
	medicine = cur.fetchone()
	cur.close()

	if int(medicine['quantityAvailable'])>=int(quantity) and patient['status'] != 'Discharged':
		curr=mysql.connection.cursor()
		result = curr.execute("update medicinesmaster set quantityAvailable = quantityAvailable - %s where medicineId=%s",(quantity,mId))
		mysql.connection.commit()
		curr.close()
	
		cur =  mysql.connection.cursor()
		res = cur.execute("insert into medicinepatient(patientId,medicineId,quantityIssued) values(%s, %s, %s)",(pId,mId,quantity))
		cur.connection.commit();
		cur.close()
		flash('Medicine issued successfully','success')

	elif patient['status'] == 'Discharged':
		flash('Patient already discharged. Can not add medicine!','danger')

	else:
		flash('Amount Exceeded, Medicine Issue failed!','danger')

	return redirect(url_for('medicines_section',id=pId))

#DIAGNOSTICS

# REad

@app.route('/diagnostics/all')
@is_logged_in
def all_diagnostics():
	cur = mysql.connection.cursor()
	result = cur.execute("select * from diagnosticsmaster")
	diagnostics = cur.fetchall()
	return render_template('all_diagnostics.html',diagnostics=diagnostics)

#search via patient id

@app.route('/patient/diagnostics',methods=['GET','POST'])
@is_logged_in
def get_patient_diagnostics():
	form = SearchPatientForm()
	if request.method == 'POST':
		_id = form.patientID.data
		cur = mysql.connection.cursor()
		result = cur.execute("select * from patients where patientId=%s",[_id])
		patient = cur.fetchone()
		cur.close()
		if result>0:
			return redirect(url_for('diagnostics_section',id=_id))
			# return render_template('medicines_dashboard.html', patient = patient)
		else:
			flash('No such user exists!','danger');

	return render_template('search_patient_diagnostic.html',form=form)

# diagnostic page of patient

@app.route('/patient/<string:id>/diagnostics',methods=['GET','POST'])
@is_logged_in
def diagnostics_section(id):
	cur = mysql.connection.cursor()
	result = cur.execute("select * from patients where patientId=%s",[id])
	patient = cur.fetchone()
	cur.close()
	curr = mysql.connection.cursor()
	result = curr.execute("select diagnosticsmaster.testName, diagnosticsmaster.testCharge from diagnosticpatient inner join diagnosticsmaster on diagnosticpatient.testId=diagnosticsmaster.testId where patientId=%s",[id])
	diagnostics = curr.fetchall()
	return render_template('diagnostics_dashboard.html',patient=patient,diagnostics = diagnostics)

# search test via id

@app.route('/patient/<string:id>/diagnostics/add',methods=['GET','POST'])
@is_logged_in
def add_diagnostics(id):
	form = SearchDiagnosticsForm()
	if request.method == 'POST':
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

# issue test to patient page

@app.route('/addDiagnostic/<string:dId>/patient/<string:pId>',methods=['POST'])
@is_logged_in
def add_diagnostic_to_patient(dId,pId):

	cur = mysql.connection.cursor()
	res = cur.execute('select * from patients where patientId = %s',[pId])
	patient = cur.fetchone()
	cur.close()

	if patient['status'] == 'Discharged':
		flash('Patient is already discharged. Could not add the test!','danger')

	else:
		cur = mysql.connection.cursor()
		res = cur.execute("select * from diagnosticsmaster where testId = %s",[dId])
		diagnostic = cur.fetchone()
		cur.close()

		cur =  mysql.connection.cursor()
		res = cur.execute("insert into diagnosticpatient(patientId,testId) values(%s, %s)",(pId,dId))
		cur.connection.commit();
		cur.close()
		flash('Test issued successfully','success')
		

	return redirect(url_for('diagnostics_section',id=pId))

#BILLING

# billing page and payment confirmation

@app.route('/patient/<string:pId>/billing',methods=['GET','POST'])
@is_logged_in
def billing_screen(pId):
	if request.method == 'POST':
		doj = datetime.now()
		cur =mysql.connection.cursor()
		result = cur.execute('update patients set status = %s, dateOfDischarge = %s where patientId = %s',('Discharged',doj,pId))
		mysql.connection.commit()
		cur.close()
		flash('Billing Confirmation done','success')
		return redirect(url_for('billing_screen',pId=pId))
	else:	
		cur = mysql.connection.cursor()
		res = cur.execute("select * from patients where patientId = %s",[pId])
		patient = cur.fetchone()
		cur.close()
		if patient['dateOfDischarge']:
			current_time = patient['dateOfDischarge']
		else:
			current_time = datetime.now()
		app.logger.info(current_time)
		_array = str(current_time - patient['dateOfAdmission']).split(' ')
		if len(_array)==1 :
			difference = 1
		else :
			difference = int(_array[0])
		if patient['typeOfBed'] == 'Single Room':
			roomFee = 8000*difference
		elif patient['typeOfBed'] == 'Semi Sharing':
			roomFee = 4000*difference
		else:
			roomFee = 2000*difference

		curr = mysql.connection.cursor()
		result = curr.execute("select diagnosticsmaster.testName, diagnosticsmaster.testCharge from diagnosticpatient inner join diagnosticsmaster on diagnosticpatient.testId=diagnosticsmaster.testId where patientId=%s",[pId])
		diagnostics = curr.fetchall()
		curr.close()

		curr = mysql.connection.cursor()
		result = curr.execute("select SUM(diagnosticsmaster.testCharge) as diagSum from diagnosticpatient inner join diagnosticsmaster on diagnosticpatient.testId=diagnosticsmaster.testId where patientId=%s",[pId])
		diagnosticTotal = curr.fetchone()
		if diagnosticTotal['diagSum'] == None:
			diagnosticTotal['diagSum'] = 0
		curr.close()

		currr = mysql.connection.cursor()
		result = currr.execute("select SUM(medicinesmaster.rateOfMedicine * medicinepatient.quantityIssued) as medSum from medicinepatient inner join medicinesmaster on medicinepatient.medicineId=medicinesmaster.medicineId where patientId=%s",[pId])
		medicineTotal = currr.fetchone()
		if medicineTotal['medSum'] == None:
			medicineTotal['medSum'] = 0

		currr.close()

		currr = mysql.connection.cursor()
		result = currr.execute("select medicinesmaster.medicineName, medicinesmaster.rateOfMedicine,medicinepatient.quantityIssued from medicinepatient inner join medicinesmaster on medicinepatient.medicineId=medicinesmaster.medicineId where patientId=%s",[pId])
		medicines = currr.fetchall()
		currr.close()
		return render_template('billing.html',patient=patient,difference=difference,roomFee=roomFee,medicines = medicines, diagnostics = diagnostics,medicineTotal=medicineTotal['medSum'],diagnosticTotal=diagnosticTotal['diagSum'])


