from flask import redirect, url_for, Response, session, render_template, request, flash
from application import app, mysql
from application.form import SearchDiagnosticsForm, SearchMedicinesForm, LoginForm, CreatePatientForm, DeletePatientForm, UpdatePatientForm, SearchPatientForm
from application.middlewares import is_logged_in, is_not_logged_in
from datetime import datetime

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login',methods=['GET','POST'])
@is_not_logged_in
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		#cursor
		curr = mysql.connection.cursor()
		#get user by username
		result = curr.execute("SELECT * FROM userstore WHERE login = %s",[username])

		app.logger.info(result)

		if(result>0):
			data = curr.fetchone()
			if password == data['password']:
				session['logged_in'] = True
				session['username'] = username
				session['name'] = 'Admin'
				flash('Logged in successfully', 'success')
				return redirect(url_for('index'))
			else:
				app.logger.info('password mismatch')
				flash('Invalid Username/Password','danger')
			curr.close()
		else:
			app.logger.info('password mismatch')
			flash('Invalid Username/Password','danger')

		return redirect(url_for('login'))	
	else:
		form = LoginForm()
		return render_template('login.html', form = form)

#Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('Logged out successfully !','success')
    return redirect(url_for('login'))

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

		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO patients(patientSsnId,patientName,age,dateOfAdmission,address,state,city,typeOfBed,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(patientSsnId,patientName,age,dateOfAdmission,address,state,city,typeOfBed,status))
		mysql.connection.commit()
		cur.close()
		flash('Patient created successfully!','success')
		return redirect(url_for('view_patient'))
	return render_template('create_patient.html', form = form)

@app.route('/view_patient', methods = ['GET', 'POST'])
@is_logged_in
def view_patient():
	cur = mysql.connection.cursor()
	cur.execute("select * from patients")
	data=cur.fetchall()
	app.logger.info(data)
	return render_template('view_patient.html', data = data)


@app.route('/patient/<string:id>/destroy',methods=['GET','POST'])
@is_logged_in
def destroy_patient(id):
	if request.method == 'POST':
		data = id
		cur = mysql.connection.cursor()
		result = cur.execute("delete from patients where patientSsnId=%s",[data])
		mysql.connection.commit()
		cur.close()
		if(result > 0):
			flash('Patient deleted successfully!','success')
			return redirect(url_for('view_patient'))
		else:
			flash('User does not exist','danger')
			return redirect(url_for('get_delete_patient'))
	return redirect(url_for('get_delete_patient'))


@app.route('/delete_patient', methods = ['GET', 'POST'])
@is_logged_in
def get_delete_patient():
	form = DeletePatientForm()
	if request.method == 'POST':
		data = form.patientSSNID.data
		cur = mysql.connection.cursor()
		result = cur.execute("select * from patients where patientSsnId=%s",[data])
		patient = cur.fetchone()
		cur.close()
		if(result > 0):
			flash('Patient found','success')
			return render_template('delete_patient.html',form=form,patient=patient)
		else:
			flash('Patient does not exist','danger')
			return redirect(url_for('get_delete_patient'))
	return render_template('delete_patient.html', form = form)


@app.route('/update_patient', methods = ['GET', 'POST'])
@is_logged_in
def update_patient():
	form = UpdatePatientForm()
	if request.method == 'POST':
		data = form.patientSSNID.data
		return redirect(url_for('create_patient_update', dataupdate = data))
	return render_template('update_patient.html', form = form)

@app.route('/create_patient_update', methods = ['GET', 'POST'])
@is_logged_in
def create_patient_update():
	ssnid = request.args.get('dataupdate')
	cur = mysql.connection.cursor()
	result = cur.execute("select *from patients where patientSsnId=%s",[ssnid])
	patient = cur.fetchone()
	app.logger.info(patient)
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
			# app.logger.info(request.form)
			# app.logger.info(form)
			
			#create cursor
			curr = mysql.connection.cursor()

		    #Execute
			curr.execute("UPDATE patients SET patientName=%s, age=%s, address=%s, dateOfAdmission=%s, typeOfBed=%s, city=%s, state=%s WHERE patientSsnId=%s",(patientName,age,address,dateOfAdmission,typeOfBed,city,state,ssnid))
			#curr.execute("UPDATE patients SET age=%s WHERE patientSsnId=%s",(age,ssnid))
		    #Commit
			mysql.connection.commit()

		    #Close Connection
			curr.close()

			flash('Patient details have been updated!','success')

			return redirect(url_for('view_patient'))

		else:
			flash('No such Patient found','danger')
			return redirect(url_for('update_patient'))

	if result>0:
		form.patientSSNID.data = patient['patientSsnId']
		form.patientName.data = patient['patientName']
		form.patientAge.data = patient['age']
		form.address.data = patient['address']
		form.dateOfAdmission.data = patient['dateOfAdmission']
		form.typeOfBed.data = patient['typeOfBed']
		form.city.data = patient['city']
		form.state.data = patient['state']
		return render_template('update_patient_by_id.html', form = form)
	else:
		flash('No such Patient found','danger')
		return redirect(url_for('update_patient'))

@app.route('/search_patient', methods = ['GET', 'POST'])
@is_logged_in
def search_patient():
	form = SearchPatientForm()
	if request.method == 'POST':
		ssnid = form.patientSSNID.data
		cur = mysql.connection.cursor()
		result = cur.execute("select *from patients where patientSsnId=%s",[ssnid])
		patient = cur.fetchone()
		cur.close()
		app.logger.info(patient)
		if result>0:
			flash('Patient found','success')
			return render_template('search_patient_by_id.html', patient = patient)
		else:
			flash('No such user exists!','danger');
	return render_template('search_patient.html', form = form)


@app.route('/medicines/all')
@is_logged_in
def all_medicines():
	cur = mysql.connection.cursor()
	result = cur.execute("select * from medicinesmaster")
	medicines = cur.fetchall()
	return render_template('all_medicines.html',medicines=medicines)

@app.route('/diagnostics/all')
@is_logged_in
def all_diagnostics():
	cur = mysql.connection.cursor()
	result = cur.execute("select * from diagnosticsmaster")
	diagnostics = cur.fetchall()
	return render_template('all_diagnostics.html',diagnostics=diagnostics)


@app.route('/patient/medicines',methods=['GET','POST'])
@is_logged_in
def get_patient_medicine():
	form = SearchPatientForm()
	if request.method == 'POST':
		ssnid = form.patientSSNID.data
		cur = mysql.connection.cursor()
		result = cur.execute("select *from patients where patientSsnId=%s",[ssnid])
		patient = cur.fetchone()
		cur.close()
		app.logger.info(patient)
		if result>0:
			return redirect(url_for('medicines_section',id=ssnid))
			# return render_template('medicines_dashboard.html', patient = patient)
		else:
			flash('No such user exists!','danger');

	return render_template('search_patient_medicine.html',form=form)

@app.route('/patient/<string:id>/medicines',methods=['GET','POST'])
@is_logged_in
def medicines_section(id):
	cur = mysql.connection.cursor()
	result = cur.execute("select * from patients where patientSsnId=%s",[id])
	patient = cur.fetchone()
	# app.logger.info(patient)
	cur.close()
	curr = mysql.connection.cursor()
	result = curr.execute("select medicinesmaster.medicineName, medicinesmaster.rateOfMedicine,medicinepatient.quantityIssued from medicinepatient inner join medicinesmaster on medicinepatient.medicineId=medicinesmaster.medicineId where patientId=%s",[id])
	medicines = curr.fetchall()
	app.logger.info(medicines)
	curr.close()
	return render_template('medicines_dashboard.html',patient=patient,medicines=medicines)

@app.route('/patient/<string:id>/medicines/add',methods=['GET','POST'])
@is_logged_in
def add_medicines(id):
	form = SearchMedicinesForm()
	if request.method == 'POST':
		medicineId = form.medicineId.data
		app.logger.info(medicineId)
		cur = mysql.connection.cursor()
		result = cur.execute("select * from medicinesmaster where medicineId=%s",[medicineId])
		medicine = cur.fetchone()
		app.logger.info(medicine)
		cur.close()
		if result>0 and medicine['quantityAvailable']>0 :
			flash('Available in stock','success')
		elif result<=0 :
			flash('Medicine does not exist with this ID','danger')
		else:
			flash('Not Available in Stock','danger')
		return render_template('add_medicines.html',form=form,medicine = medicine,id=id)
	return render_template('add_medicines.html',form=form)

@app.route('/addMedicine/<string:mId>/patient/<string:pId>',methods=['POST'])
@is_logged_in
def addMedicineToPatient(mId,pId):
	quantity = int(request.form['quantity'])
	cur = mysql.connection.cursor()
	res = cur.execute("select * from medicinesmaster where medicineId = %s",[mId])
	medicine = cur.fetchone()
	cur.close()
	if int(medicine['quantityAvailable'])>=int(quantity):
		curr=mysql.connection.cursor()
		result = curr.execute("update medicinesmaster set quantityAvailable = quantityAvailable - %s where medicineId=%s",(quantity,mId))
		mysql.connection.commit()
		curr.close()
	
		cur =  mysql.connection.cursor()
		res = cur.execute("insert into medicinepatient(patientId,medicineId,quantityIssued) values(%s, %s, %s)",(pId,mId,quantity))
		cur.connection.commit();
		cur.close()
		flash('Medicine issued successfully','success')
	else:
		flash('Amount Exceeded, Medicine Issue failed!','danger')

	return redirect(url_for('medicines_section',id=pId))


@app.route('/patient/diagnostics',methods=['GET','POST'])
@is_logged_in
def get_patient_diagnostics():
	form = SearchPatientForm()
	if request.method == 'POST':
		ssnid = form.patientSSNID.data
		cur = mysql.connection.cursor()
		result = cur.execute("select * from patients where patientSsnId=%s",[ssnid])
		patient = cur.fetchone()
		cur.close()
		app.logger.info(patient)
		if result>0:
			return redirect(url_for('diagnostics_section',id=ssnid))
			# return render_template('medicines_dashboard.html', patient = patient)
		else:
			flash('No such user exists!','danger');

	return render_template('search_patient_diagnostic.html',form=form)

@app.route('/patient/<string:id>/diagnostics',methods=['GET','POST'])
@is_logged_in
def diagnostics_section(id):
	cur = mysql.connection.cursor()
	result = cur.execute("select * from patients where patientSsnId=%s",[id])
	patient = cur.fetchone()
	app.logger.info(patient)
	cur.close()
	curr = mysql.connection.cursor()
	result = curr.execute("select diagnosticsmaster.testName, diagnosticsmaster.testCharge from diagnosticpatient inner join diagnosticsmaster on diagnosticpatient.testId=diagnosticsmaster.testId where patientId=%s",[id])
	diagnostics = curr.fetchall()
	app.logger.info(diagnostics)
	return render_template('diagnostics_dashboard.html',patient=patient,diagnostics = diagnostics)


@app.route('/patient/<string:id>/diagnostics/add',methods=['GET','POST'])
@is_logged_in
def add_diagnostics(id):
	form = SearchDiagnosticsForm()
	if request.method == 'POST':
		testId = form.testId.data
		cur = mysql.connection.cursor()
		result = cur.execute("select * from diagnosticsmaster where testId=%s",[testId])
		diagnostic = cur.fetchone()
		cur.close()
		if result>0 :
			flash('Test Available','success')
		else :
			flash('Test does not exist with this ID','danger')
		return render_template('add_diagnostics.html',form=form,diagnostic = diagnostic,id=id)
	return render_template('add_diagnostics.html',form=form)

@app.route('/addDiagnostic/<string:dId>/patient/<string:pId>',methods=['POST'])
@is_logged_in
def add_diagnostic_to_patient(dId,pId):
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

@app.route('/patient/<string:pId>/billing',methods=['GET','POST'])
@is_logged_in
def billing_screen(pId):
	if request.method == 'POST':
		doj = datetime.now()
		cur =mysql.connection.cursor()
		result = cur.execute('update patients set status = %s, dateOfDischarge = %s where patientSsnId = %s',('Discharged',doj,pId))
		mysql.connection.commit()
		cur.close()
		flash('Billing Confirmation done','success')
		return redirect(url_for('billing_screen',pId=pId))
	else:	
		cur = mysql.connection.cursor()
		res = cur.execute("select * from patients where patientSsnId = %s",[pId])
		patient = cur.fetchone()
		cur.close()
		current_time = datetime.now()
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
		app.logger.info(diagnostics)
		curr.close()

		curr = mysql.connection.cursor()
		result = curr.execute("select SUM(diagnosticsmaster.testCharge) as diagSum from diagnosticpatient inner join diagnosticsmaster on diagnosticpatient.testId=diagnosticsmaster.testId where patientId=%s",[pId])
		diagnosticTotal = curr.fetchone()
		if diagnosticTotal['diagSum'] == None:
			diagnosticTotal['diagSum'] = 0
		app.logger.info(diagnosticTotal)
		curr.close()

		currr = mysql.connection.cursor()
		result = currr.execute("select SUM(medicinesmaster.rateOfMedicine * medicinepatient.quantityIssued) as medSum from medicinepatient inner join medicinesmaster on medicinepatient.medicineId=medicinesmaster.medicineId where patientId=%s",[pId])
		medicineTotal = currr.fetchone()
		if medicineTotal['medSum'] == None:
			medicineTotal['medSum'] = 0

		app.logger.info(medicineTotal)
		currr.close()

		currr = mysql.connection.cursor()
		result = currr.execute("select medicinesmaster.medicineName, medicinesmaster.rateOfMedicine,medicinepatient.quantityIssued from medicinepatient inner join medicinesmaster on medicinepatient.medicineId=medicinesmaster.medicineId where patientId=%s",[pId])
		medicines = currr.fetchall()
		app.logger.info(medicines)
		currr.close()
		return render_template('billing.html',patient=patient,difference=difference,roomFee=roomFee,medicines = medicines, diagnostics = diagnostics,medicineTotal=medicineTotal['medSum'],diagnosticTotal=diagnosticTotal['diagSum'])


