from flask import session, flash, url_for, redirect
from functools import wraps

# To check the login status 

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorised, Please Login','danger')
            return redirect(url_for('login'))
    return wrap

def is_not_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return redirect(url_for('index'))
        else:
             return f(*args, **kwargs)
            
    return wrap
