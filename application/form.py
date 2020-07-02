from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

class LoginForm(FlaskForm):
	username = StringField("Email", validators=[DataRequired(),Length(min=5)])
	password = PasswordField("Password", validators = [DataRequired()])
	submit = SubmitField("Login")

class CreatePatientForm(FlaskForm):
	patientSSNID = IntegerField("Patient SSN ID (9 digits)",validators = [DataRequired(), length])
	patientName = StringField("Patient Name",validators = [DataRequired(),alphabetic])
	patientAge = IntegerField("Patient Age",validators = [DataRequired(), agelength])
	dateOfAdmission = DateField("Date of Admission",validators = [])
	typeOfBed = SelectField("Type of Bed", choices=["General Ward", "Semi Sharing", "Single Room"],validators = [DataRequired()])
	address  = TextAreaField("Address",validators = [DataRequired()])
	state = StringField("State",validators = [DataRequired()])
	city = StringField("City",validators = [DataRequired()])
	submit = SubmitField("Register")

class UpdatePatientForm(FlaskForm):
	patientSSNID = IntegerField("Patient SSN ID",validators = [DataRequired(), length])
	submit = SubmitField("Get")

class DeletePatientForm(FlaskForm):
	patientSSNID = IntegerField("Patient SSN ID",validators = [DataRequired(), length])
	submit = SubmitField("Delete")

class SearchPatientForm(FlaskForm):
	patientSSNID = IntegerField("Patient SSN ID",validators = [DataRequired(),length])
	submit = SubmitField("Search")

class SearchMedicinesForm(FlaskForm):
	medicineName = StringField("Medicine Name",validators = [DataRequired(), alphabetic])


class SearchDiagnosticsForm(FlaskForm):
	testName = StringField("Test Name",validators = [DataRequired(), alphabetic])


def alphabetic(self, fieldName):
		flag = any(char.isdigit() for char in list(fieldName.data))
		if flag:
			raise ValidationError("Test Name contains number")

def length(self, fieldName):
		if len(list(fieldName.data)) != 9:
			raise ValidationError("SSN ID ust be 9 digit long")

def agelength(self, fieldName):
		if len(list(fieldName.data)) >0 and len(list(fieldName.data)) <=3:
			raise ValidationError("Out of order value")