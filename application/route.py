from flask import redirect, url_for, Response, render_template, request, flash
from application import app
from application.form import LoginForm, CreatePatientForm,IssueMedicineForm,GetPatientForm

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login')
def login():
	form = LoginForm()
	return render_template('login.html', form = form)

@app.route('/create_patient')
def create_patient():
	form = CreatePatientForm()
	return render_template('create_patient.html', form = form)


@app.route('/get_patient',methods=["GET","POST"])
def get_patient():
	flag=1
	form=GetPatientForm()
	if request.method=='POST':     
		pid=form.patientSSNID.data

		patient=patients.query.filter_by(patientId=pid).first_or_404(description='There is no patient having id  {}'.format(pid))

		cur = mysql.connection.cursor()

		query="select medicinesmaster.medicineName,medicinesmaster.rateOfMedicine,medicinepatient.quantityIssued from medicinepatient inner join medicinesmaster on medicinepatient.medicineId=medicinesmaster.medicineId where patientId=1"
		cur.execute("query")

		# structure>> (medcineName, rateOfMedicine, quantityIssued)
		records = cursor.fetchall()


		return render_template('get_patient.html',patient=patient,records=records,flag=1)

	else:
		form=GetPatientForm()
		return render_template('get_patient.html',form=form,flag=0)


@app.route('/issue_medicine',methods=["GET", "POST"])
def issue_medicine():
	form=IssueMedicineForm()
	if request.method == 'POST':
		medname=form.medName.data
		quantity=form.medQuantity.data

		med = medicine.query.filter_by(medname='medname').first_or_404(description='There is no medcine named {}'.format(medname))

        return render_template('issue_medicine.html',med=med,quantity=quantity)
    else    
		form= IssueMedicineForm()
		return render_template('issue_medicine.html',form=form)