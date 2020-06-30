from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

class LoginForm(FlaskForm):
	username = StringField("Email", validators = [DataRequired()])
	password = PasswordField("Password", validators = [DataRequired()])
	submit = SubmitField("Login")

class CreatePatientForm(FlaskForm):
	patientSSNID = IntegerField("Patient SSN ID",validators = [DataRequired()])
	patientName = StringField("Patient Name",validators = [DataRequired()])
	patientAge = IntegerField("Patient Age",validators = [DataRequired()])
	dateOfAdmission = DateField("Date of Admission",validators = [])
	typeOfBed = SelectField("Type of Bed", choices=["General Ward", "Semi Sharing", "Single Room"],validators = [DataRequired()])
	address  = StringField("Address",validators = [DataRequired()])
	state = StringField("State",validators = [DataRequired()])
	city = StringField("City",validators = [DataRequired()])
	submit = SubmitField("Register")

class UpdatePatientForm(FlaskForm):
	patientSSNID = IntegerField("Patient SSN ID",validators = [DataRequired()])
	submit = SubmitField("Get")

class DeletePatientForm(FlaskForm):
	patientSSNID = IntegerField("Patient SSN ID",validators = [DataRequired()])
	submit = SubmitField("Delete")

class SearchPatientForm(FlaskForm):
	patientSSNID = IntegerField("Patient SSN ID",validators = [DataRequired()])
	submit = SubmitField("Search")