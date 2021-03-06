from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

class LoginForm(FlaskForm):
	username = StringField("Email", validators=[DataRequired(),Length(min=5)])
	password = PasswordField("Password", validators = [DataRequired()])
	submit = SubmitField("Login")

class CreatePatientForm(FlaskForm):
	patientSSNID = IntegerField("Patient SSN ID (9 digits)",validators = [Length(min=9),DataRequired()])
	patientName = StringField("Patient Name",validators = [DataRequired()])
	patientAge = IntegerField("Patient Age",validators = [DataRequired()])
	dateOfAdmission = DateField("Date of Admission",validators = [])
	typeOfBed = SelectField("Type of Bed", choices=["General Ward", "Semi Sharing", "Single Room"],validators = [DataRequired()])
	address  = TextAreaField("Address",validators = [DataRequired()])
	state = StringField("State",validators = [DataRequired()])
	city = StringField("City",validators = [DataRequired()])
	submit = SubmitField("Register")

class UpdatePatientForm(FlaskForm):
	patientID = IntegerField("Patient ID",validators = [DataRequired()])
	submit = SubmitField("Get")

class DeletePatientForm(FlaskForm):
	patientID = IntegerField("Patient ID",validators = [DataRequired()])
	submit = SubmitField("Delete")

class SearchPatientForm(FlaskForm):
	patientID = IntegerField("Patient ID",validators = [DataRequired()])
	submit = SubmitField("Search")

class SearchMedicinesForm(FlaskForm):
	medicineName = StringField("Medicine Name",validators = [DataRequired()])


class SearchDiagnosticsForm(FlaskForm):
	testName = StringField("Test Name",validators = [DataRequired()])