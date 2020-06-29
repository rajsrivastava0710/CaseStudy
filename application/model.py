from application import app, db
import sqlalchemy.dialects.sqlite
from datetime import datetime

class Patient(db.Model):
	patientSSNID = db.Column(db.Integer, primary_key=True)
	patientName = db.Column(db.String(50))
	patientAge = db.Column(db.Integer)
	dateOfAdmission = db.Column(db.DateTime, default = datetime.now)
	typeOfBed = db.Column(db.String(50))
	address = db.Column(db.String(100))
	state = db.Column(db.String(50))
	city = db.Column(db.String(50))

	def __init__(self,patientSSNID,patientName,patientAge,dateOfAdmission,address,state,city,typeOfBed):
		self.patientSSNID = patientSSNID
		self.patientName = patientName
		self.patientAge = patientAge
		self.dateOfAdmission = dateOfAdmission
		self.typeOfBed = typeOfBed
		self.address = address
		self.state = state
		self.city = city