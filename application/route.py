from flask import redirect, url_for, Response, render_template, request, flash
from application import app
from application.form import LoginForm, CreatePatientForm,IssueMedicineForm,GetPatientDetails

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

@app.route('/pharmacist',methods=["GET","POST"])
def pharmacist():
	if request.method=='POST':
		pid=request.form[pid]

		patient=patients.query.filter_by(patientId=pid).first_or_404(description='There is no patient having id  {}'.format(pid))

		cur = mysql.connection.cursor()

		query="select medicinesmaster.medicineName,medicinesmaster.rateOfMedicine,medicinepatient.quantityIssued from medicinepatient inner join medicinesmaster on medicinepatient.medicineId=medicinesmaster.medicineId where patientId=1"
		cur.execute("query")

		# structure>> (medcineName, rateOfMedicine, quantityIssued)
		records = cursor.fetchall()


		return render_template('pharmacist.html',patient=patient,records=records)

	else:
		return render_template('pharmacist.html')


# @app.route('/issue_medicine',methods=["GET", "POST"])
# def issue_medicine():
# 	if request.method == 'POST':
# 		medname=request.form['medName']

# 		# write down here sql query to fetch medcine details named medNme from medicine db
# 		med = medicine.query.filter_by(medname='medname').first()
# 		flag={"available":True,"quantity"=1}

# 		if med is None:
# 			succes="no data found"
# 			return render_template('issue_medicine',success=success)

#         else if med is not None and med.quantity!=0:
#         	rate=med.rate
# 		#ammount for each medicine ,yet to 
# 		#here update current petient database with med id and med quantity
# 		#also update medicine ta
#     else:
#         return render_template('entry.html')
# 	form= IssueMedicineForm()
# 	return render_template('issue_medicine.html',form=form)