# -*- coding: utf-8 -*-

from roommates import app

from flask import session, redirect, url_for, g
from functools import wraps

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if not session.get('id'):
			return redirect(url_for('login'))
		return f(*args, **kwargs)
	return decorated_function

def login_or_test_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if not session.get('id') or not app.config['TESTING']:
			return redirect(url_for('login'))
		return f(*args, **kwargs)
	return decorated_function

def query_db(query, args=(), one=False):
	cur = g.db.execute(query, args)
	rv = [dict((cur.description[idx][0], value) for idx, value in enumerate(row)) for row in cur.fetchall()]
	return (rv[0] if rv else None) if one else rv