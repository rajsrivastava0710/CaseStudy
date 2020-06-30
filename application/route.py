from flask import redirect, url_for, Response, session, render_template, request, flash
from application import app, mysql
from application.form import LoginForm, CreatePatientForm, DeletePatientForm, UpdatePatientForm, SearchPatientForm
from application.middlewares import is_logged_in, is_not_logged_in

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
		result = curr.execute("SELECT * FROM Admin WHERE username = %s",[username])

		app.logger.info(result)

		if(result>0):
			data = curr.fetchone()
			if password == data['password']:
				app.logger.info(data['password'])
				app.logger.info('PASSWORD MATCHED')
				session['logged_in'] = True
				session['username'] = username
				session['name'] = 'Admin'
				flash('Logged in successfully', 'success')
				return redirect(url_for('index'))
			else:
				app.logger.info('password mismatch')
				flash('Invalid Username/Password')
			curr.close()
		else:
			app.logger.info('password mismatch')
			flash('Invalid Username/Password')

		redirect(url_for('login'))	
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
		# patient = Patient(patientSSNID,patientName,patientAge,dateOfAdmission,address,state,city,typeOfBed)
		# db.session.add(patient)
		# db.session.commit()
		#flash("Patient added successfully")
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO patients(patientSsnId,patientName,age,dateOfAdmission,address,state,city,typeOfBed,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'0')",(patientSsnId,patientName,age,dateOfAdmission,address,state,city,typeOfBed))
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

@app.route('/delete_patient', methods = ['GET', 'POST'])
@is_logged_in
def delete_patient():
	form = DeletePatientForm()
	if request.method == 'POST':
		data = form.patientSSNID.data
		cur = mysql.connection.cursor()
		cur.execute("delete from patients where patientSsnId=%s",[data])
		mysql.connection.commit()
		cur.close()
		flash('Patient deleted successfully!','success')
		return redirect(url_for('view_patient'))
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
			patientSsnId = form.patientSSNID.data
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
			curr.execute("UPDATE patients SET patientSsnId=%s, patientName=%s, age=%s, address=%s, dateOfAdmission=%s, typeOfBed=%s, city=%s, state=%s WHERE patientSsnId=%s",(patientSsnId,patientName,age,address,dateOfAdmission,typeOfBed,city,state,ssnid))
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
			return render_template('search_patient_by_id.html', patient = patient)
		else:
			flash('No such user exists!','danger');
	return render_template('search_patient.html', form = form)




	