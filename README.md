# WebCMS4
A sample vulnerable application

## Setup and Run
```
pip3 install -r requirements.txt
python3 run.py
```

Valid credentials: s5000001:password

## Vulnerabilities
* Blind SQLi in login form
* SQLi in course search page
* Local file inclusion in profile pic URL through directory traversal
* Command injection in assignment submission (with client-side sanitisation)
* Business logic vulnerability: uploading pic with a file name used by another user's pic replaces it
* Unrestricted file upload: unprocessed image stored on server, including GPS coordinates in EXIF data for user s5000005's pic
* Server-side template injection in update bio field (using Jinja2)
