from flask import redirect, url_for, Response, render_template, request, flash
from application import app, db
from application.form import LoginForm, CreatePatientForm, DeletePatientForm, UpdatePatientForm, SearchPatientForm
from application.model import Patient

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login')
def login():
	form = LoginForm()
	return render_template('login.html', form = form)

@app.route('/create_patient', methods = ['GET', 'POST'])
def create_patient():
	form = CreatePatientForm()
	if request.method == 'POST':
		patientSSNID = form.patientSSNID.data
		patientName = form.patientName.data
		patientAge = form.patientAge.data
		dateOfAdmission = form.dateOfAdmission.data
		address = form.address.data
		state = form.state.data
		city = form.city.data
		typeOfBed = form.typeOfBed.data
		patient = Patient(patientSSNID,patientName,patientAge,dateOfAdmission,address,state,city,typeOfBed)
		db.session.add(patient)
		db.session.commit()
		#flash("Patient added successfully")
		return redirect(url_for('view_patient'))
	return render_template('create_patient.html', form = form)

@app.route('/view_patient', methods = ['GET', 'POST'])
def view_patient():
	return render_template('view_patient.html', data = Patient.query.all())

@app.route('/delete_patient', methods = ['GET', 'POST'])
def delete_patient():
	form = DeletePatientForm()
	if request.method == 'POST':
		data = form.patientSSNID.data
		db.session.delete(Patient.query.get(data))
		db.session.commit()
		return redirect(url_for('view_patient'))
	return render_template('delete_patient.html', form = form)

@app.route('/update_patient', methods = ['GET', 'POST'])
def update_patient():
	form = UpdatePatientForm()
	if request.method == 'POST':
		data = form.patientSSNID.data
		return redirect(url_for('create_patient_update', dataupdate = data))
	return render_template('update_patient.html', form = form)

@app.route('/create_patient<dataupdate>', methods = ['GET', 'POST'])
def create_patient_update(dataupdate):
	patient = Patient.query.get(dataupdate)
	form = CreatePatientForm()
	if request.method == "POST":
		patient.patientSSNID = form.patientSSNID.data
		patient.patientName = form.patientName.data
		patient.patientAge = form.patientAge.data
		patient.address = form.address.data
		patient.dateOfAdmission = form.dateOfAdmission.data
		patient.typeOfBed = form.typeOfBed.data
		patient.city = form.city.data
		patient.state = form.state.data
		db.session.commit()
		return redirect(url_for('view_patient'))
	form.patientSSNID.data = patient.patientSSNID
	form.patientName.data = patient.patientName
	form.patientAge.data = patient.patientAge
	form.address.data = patient.address
	form.dateOfAdmission.data = patient.dateOfAdmission
	form.typeOfBed.data = patient.typeOfBed
	form.city.data = patient.city
	form.state.data = patient.state
	return render_template('create_patient.html', form = form)

@app.route('/search_patient', methods = ['GET', 'POST'])
def serach_patient():
	form = SearchPatientForm()
	if request.method == 'POST':
		data = form.patientSSNID.data
		d = Patient.query.get(data)
		print(data)
		return render_template('search_patient_by_id.html', d = d)
	return render_template('search_patient.html', form = form)




	