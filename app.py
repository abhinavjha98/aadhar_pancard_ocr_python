import os,io
from google.cloud import vision
from google.cloud.vision import types
import pandas as pd
from werkzeug.utils import secure_filename
import pyrebase
from firebase import firebase
from flask import *
import pandas as pd
app = Flask(__name__)
app.secret_key = "hello"


config = {
	"apiKey": "AIzaSyAYeR8EbGT8o0mkcqpiL6s7PfcCrT2_naA",
    "authDomain": "sih2020-59356.firebaseapp.com",
    "databaseURL": "https://sih2020-59356.firebaseio.com",
    "projectId": "sih2020-59356",
    "storageBucket": "sih2020-59356.appspot.com",
    "messagingSenderId": "40198112981",
    "appId": "1:40198112981:web:8768d7a572404c1b7c845c",
    "measurementId": "G-2NW3KXNK42",
    "serviceAccount": "serviceAccount.json"
}



FBConn = firebase.FirebaseApplication('https://sih2020-59356.firebaseio.com')

firebase = pyrebase.initialize_app(config)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ServiceAccount.json'
client = vision.ImageAnnotatorClient()

file_name = 'pan.jpeg'
image_path = f'E:\PROJECT\\aadhar_OCR\{file_name}'

with io.open(image_path, 'rb') as image_file:
		content = image_file.read()

image = vision.types.Image(content=content)
response = client.text_detection(image=image,  image_context={"language_hints": ["en"]})
texts = response.text_annotations
df = pd.DataFrame(columns=['locale', 'description'])

for text in texts:
		df = df.append(
					dict(
				locale=text.locale,
				description=text.description
				),
 				ignore_index=True
		)
# data_text=[]
# for i in df:
# 	data_text.append(df[i][0])

# print(df['description'][0])
# print(data_text)


@app.route('/',methods=["GET","POST"])
def pan():
	a=""
	if request.method == "POST":
		if request.form['upload']=="Upload":
			upload = request.files['upload']
			filename = secure_filename(upload.filename)
			print(filename)
			file_name = filename
			image_path = f'E:\PROJECT\\aadhar_OCR\{file_name}'

			with io.open(image_path, 'rb') as image_file:
				content = image_file.read()

			image = vision.types.Image(content=content)
			response = client.text_detection(image=image,  image_context={"language_hints": ["en"]})
			texts = response.text_annotations
			df = pd.DataFrame(columns=['locale', 'description'])

			for text in texts:
				df = df.append(
					dict(
				locale=text.locale,
				description=text.description
				),
 				ignore_index=True
				)
				
				a = df['description'][0]
				a = "INCOME TAX DEPARTMENT GOVT. OF INDIA Permanent Account Number Card BRQPJ9191M / Name ABHINAV JHA frar a Father's Name DHEERAJKUMAR JHA a a h Date of Birth F Signature 28/12/1998 19052018"
				b = a.split("Permanent Account Number Card ")
				c = b[1].split(" /")
				print("Pan card Number :",c[0])

				d = a.split(" / Name ")
				e = d[1].split(" ")
				name_of_person = e[0]+" "+ e[1]
				print("Name: "+e[0]+" "+ e[1])

				f = a.split("Father's Name ")
				g = f[1].split(" ")
				father =g[0]+" "+g[1]
				print("Fathers Name : "+g[0]+" "+g[1])

				import re
				from datetime import datetime

				match = re.search(r'\d{2}/\d{2}/\d{4}',a)
				date = datetime.strptime(match.group(), '%d/%m/%Y').date()
				print(date)
			result = FBConn.post('/pan_card/', a)
	return render_template('pan.html',a=a,name=name_of_person,father=father,pancard = c[0],datee=date)


if __name__ == '__main__':
	app.run(debug=True)
