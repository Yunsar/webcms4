from flask import *
from server import app
from webcms4db import Course, User

from urllib.parse import urlparse

import subprocess
import requests
import os

@app.route("/")
def index():
	if session.get("sid") is None:
		return redirect("/login");

	user = User.get_user(session.get("sid"))

	return render_template("index.html", user=user)

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		if User.check_creds(request.form.get("sid"), request.form.get("password")):
			session["sid"] = request.form.get("sid")
			return redirect("/")
		else:
			return render_template("login.html", error="Invalid credentials")

	return render_template("login.html")

@app.route("/logout")
def logout():
	session.pop("sid")
	return redirect("/login")

@app.route("/courses", methods=["GET", "POST"])
def courses():
	search = request.form.get("search", "")
	courses = Course.get_query(search)

	return render_template("courses.html", search=search, courses=courses)

@app.route("/profile/<sid>")
def profile(sid):
	if session.get("sid") is None:
		return redirect("/login");

	user = User.get_user(session.get("sid"))

	prof = User.get_user(sid)
	if prof is None:
		abort(404)

	return render_template_string(render_template("profile.html", user=user, 
			name=prof[1], image=prof[2], bio=prof[3], edit=user[0]==prof[0]))

@app.route("/profile/<sid>/edit", methods=["GET", "POST"])
def edit_profile(sid):
	if session.get("sid") is None:
		return redirect("/login");

	user = User.get_user(session.get("sid"))

	if sid != user[0]:
		abort(403)
	
	if request.method == "POST":
		url = request.form.get("url", "").strip()
		if url:
			filepath = "images/" + os.path.basename(urlparse(url).path)
			res = requests.get(url, allow_redirects=True)

			with open(filepath, "wb") as f:
				f.write(res.content)

			User.update_image(sid, filepath)

		User.update_bio(sid, request.form.get("bio", ""))
		user = User.get_user(sid)
		return render_template("edit_profile.html", user=user, update=True)

	return render_template("edit_profile.html", user=user)

@app.route("/outline")
def outline():
	if session.get("sid") is None:
		return redirect("/login");

	user = User.get_user(session.get("sid"))

	return render_template("outline.html", user=user)

@app.route("/getimage")
def getimage():
	return send_file(request.args.get("image"))

@app.route("/assignments", methods=["GET", "POST"])
def assignments():
	if session.get("sid") is None:
		return redirect("/login");

	user = User.get_user(session.get("sid"))

	if request.method == "POST":
		assign = request.form.get("assignment", "")
		output = subprocess.check_output(["sh", "-c", "./checksubmission.sh " + 
				assign]).decode()
		return render_template("assignments.html", user=user, assignment=assign, 
				output=output)

	return render_template("assignments.html", user=user, assignment="assignment1")
	
		

