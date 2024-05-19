from flask import Flask, request,render_template, redirect,session
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required,LoginManager
import bcrypt
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
import os
import io
import base64
import matplotlib
matplotlib.use('Agg')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self,email,password,name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def generate_pie_chart(data):

    max_length = 20
    locations = [loc[:max_length] + "..." if len(loc) > max_length else loc for loc in data.index.to_numpy()]

    plt.figure(figsize=(8, 8))
    plt.pie(data.to_numpy(), labels=locations, autopct='%1.1f%%', startangle=90, pctdistance=0.85)
    plt.title("Accident Distribution by Accident Location")
    plt.gca().add_artist(plt.Circle((0, 0), 0.70, fc='white'))
    plt.tight_layout()

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    plt.close()  # Close the figure to avoid memory leaks

    img_data = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_data}"

def generate_line_chart(data):

    plt.figure(figsize=(12, 6))
    plt.plot(data['DISTRICTNAME'], data['TotalAccidents'], marker='o', linestyle='-')
    plt.title('Total Accidents per District')
    plt.xlabel('District')
    plt.ylabel('Total Accidents')
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.tight_layout()

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    plt.close()  # Close the figure to avoid memory leaks

    img_data = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_data}"

def generate_bar_chart(data):

    plt.figure(figsize=(10, 6))
    data.plot(kind='bar', color='skyblue')
    plt.xlabel('Road Type')
    plt.ylabel('Accident Count')
    plt.title('Accident Distribution by Road Type')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y')
    plt.tight_layout()

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    plt.close()  # Close the figure to avoid memory leaks

    img_data = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_data}"

def generate_chart_data():
    data = pd.read_csv('main.csv')
    bengaluru_data = data[data['DISTRICTNAME'] == 'Bengaluru City']

    # Top 15 places with more accidents
    top_units_counts = bengaluru_data['UNITNAME'].value_counts().head(15)
    top_units_labels = top_units_counts.index.tolist()
    top_units_data = top_units_counts.tolist()

    # Types of Roads where Accidents Occur
    road_type_counts = bengaluru_data['Road_Type'].value_counts()
    road_type_labels = road_type_counts.index.tolist()
    road_type_data = road_type_counts.tolist()

    return top_units_labels, top_units_data, road_type_labels, road_type_data



@app.route('/bangalore',methods=['GET','POST'])
def bangalore():
    data = pd.read_csv('main.csv')
    bengaluru_data = data[data['DISTRICTNAME'] == 'Bengaluru City']

    # Top 15 places with more accidents
    top_units_counts = bengaluru_data['UNITNAME'].value_counts().head(15)
    top_units_labels = top_units_counts.index.tolist()
    top_units_data = top_units_counts.tolist()

    # Types of Roads where Accidents Occur
    road_type_counts = bengaluru_data['Road_Type'].value_counts()
    road_type_labels = road_type_counts.index.tolist()
    road_type_data = road_type_counts.tolist()

    return render_template('./districts/bangalore.html', top_units_labels=top_units_labels,
                            top_units_data=top_units_data,
                            road_type_labels=road_type_labels,
                            road_type_data=road_type_data,
                            accident_counts=accident_counts, suggestions=suggestions)


@app.route('/bagalkot',methods=['GET','POST'])

def bagalkot():
    data = pd.read_csv('main.csv')
    bengaluru_data = data[data['DISTRICTNAME'] == 'Bagalkot']

    # Top 15 places with more accidents
    top_units_counts = bengaluru_data['UNITNAME'].value_counts().head(15)
    top_units_labels = top_units_counts.index.tolist()
    top_units_data = top_units_counts.tolist()

    # Types of Roads where Accidents Occur
    road_type_counts = bengaluru_data['Road_Type'].value_counts()
    road_type_labels = road_type_counts.index.tolist()
    road_type_data = road_type_counts.tolist()

    return render_template('./districts/bagalkot.html', top_units_labels=top_units_labels,
                            top_units_data=top_units_data,
                            road_type_labels=road_type_labels,
                            road_type_data=road_type_data,
                            accident_counts=accident_counts, suggestions=suggestions)


@app.route('/Chikkamagaluru',methods=['GET','POST'])

def Chikkamagaluru():
    data = pd.read_csv('main.csv')
    bengaluru_data = data[data['DISTRICTNAME'] == 'Chikkamagaluru']

    # Top 15 places with more accidents
    top_units_counts = bengaluru_data['UNITNAME'].value_counts().head(15)
    top_units_labels = top_units_counts.index.tolist()
    top_units_data = top_units_counts.tolist()

    # Types of Roads where Accidents Occur
    road_type_counts = bengaluru_data['Road_Type'].value_counts()
    road_type_labels = road_type_counts.index.tolist()
    road_type_data = road_type_counts.tolist()

    return render_template('./districts/Chikkamagaluru.html', top_units_labels=top_units_labels,
                            top_units_data=top_units_data,
                            road_type_labels=road_type_labels,
                            road_type_data=road_type_data,
                            accident_counts=accident_counts, suggestions=suggestions)


@app.route('/Davanagere',methods=['GET','POST'])

def Davanagere():
    data = pd.read_csv('main.csv')
    bengaluru_data = data[data['DISTRICTNAME'] == 'Davanagere']

    # Top 15 places with more accidents
    top_units_counts = bengaluru_data['UNITNAME'].value_counts().head(15)
    top_units_labels = top_units_counts.index.tolist()
    top_units_data = top_units_counts.tolist()

    # Types of Roads where Accidents Occur
    road_type_counts = bengaluru_data['Road_Type'].value_counts()
    road_type_labels = road_type_counts.index.tolist()
    road_type_data = road_type_counts.tolist()

    return render_template('./districts/Davanagere.html', top_units_labels=top_units_labels,
                            top_units_data=top_units_data,
                            road_type_labels=road_type_labels,
                            road_type_data=road_type_data,
                            accident_counts=accident_counts, suggestions=suggestions)

@app.route('/kgf',methods=['GET','POST'])

def kgf():
    data = pd.read_csv('main.csv')
    bengaluru_data = data[data['DISTRICTNAME'] == 'K.G.F']

    # Top 15 places with more accidents
    top_units_counts = bengaluru_data['UNITNAME'].value_counts().head(15)
    top_units_labels = top_units_counts.index.tolist()
    top_units_data = top_units_counts.tolist()

    # Types of Roads where Accidents Occur
    road_type_counts = bengaluru_data['Road_Type'].value_counts()
    road_type_labels = road_type_counts.index.tolist()
    road_type_data = road_type_counts.tolist()

    return render_template('./districts/kgf.html', top_units_labels=top_units_labels,
                            top_units_data=top_units_data,
                            road_type_labels=road_type_labels,
                            road_type_data=road_type_data,
                            accident_counts=accident_counts, suggestions=suggestions)


@app.route('/Mangaluru',methods=['GET','POST'])

def Mangaluru():
    data = pd.read_csv('main.csv')
    bengaluru_data = data[data['DISTRICTNAME'] == 'Mangaluru City']

    # Top 15 places with more accidents
    top_units_counts = bengaluru_data['UNITNAME'].value_counts().head(15)
    top_units_labels = top_units_counts.index.tolist()
    top_units_data = top_units_counts.tolist()

    # Types of Roads where Accidents Occur
    road_type_counts = bengaluru_data['Road_Type'].value_counts()
    road_type_labels = road_type_counts.index.tolist()
    road_type_data = road_type_counts.tolist()

    return render_template('./districts/Mangaluru.html', top_units_labels=top_units_labels,
                            top_units_data=top_units_data,
                            road_type_labels=road_type_labels,
                            road_type_data=road_type_data,
                            accident_counts=accident_counts, suggestions=suggestions)


@app.route('/Mysuru',methods=['GET','POST'])

def Mysuru():
    data = pd.read_csv('main.csv')
    bengaluru_data = data[data['DISTRICTNAME'] == 'Mysuru City']

    # Top 15 places with more accidents
    top_units_counts = bengaluru_data['UNITNAME'].value_counts().head(15)
    top_units_labels = top_units_counts.index.tolist()
    top_units_data = top_units_counts.tolist()

    # Types of Roads where Accidents Occur
    road_type_counts = bengaluru_data['Road_Type'].value_counts()
    road_type_labels = road_type_counts.index.tolist()
    road_type_data = road_type_counts.tolist()

    return render_template('./districts/Mysuru.html', top_units_labels=top_units_labels,
                            top_units_data=top_units_data,
                            road_type_labels=road_type_labels,
                            road_type_data=road_type_data,
                            accident_counts=accident_counts, suggestions=suggestions)

@app.route('/Udupi',methods=['GET','POST'])

def Udupi():
    data = pd.read_csv('main.csv')
    bengaluru_data = data[data['DISTRICTNAME'] == 'Udupi']

    # Top 15 places with more accidents
    top_units_counts = bengaluru_data['UNITNAME'].value_counts().head(15)
    top_units_labels = top_units_counts.index.tolist()
    top_units_data = top_units_counts.tolist()

    # Types of Roads where Accidents Occur
    road_type_counts = bengaluru_data['Road_Type'].value_counts()
    road_type_labels = road_type_counts.index.tolist()
    road_type_data = road_type_counts.tolist()

    return render_template('./districts/Udupi.html', top_units_labels=top_units_labels,
                            top_units_data=top_units_data,
                            road_type_labels=road_type_labels,
                            road_type_data=road_type_data,
                            accident_counts=accident_counts, suggestions=suggestions)


@app.route('/Vijayanagara',methods=['GET','POST'])

def Vijayanagara():
    data = pd.read_csv('main.csv')
    bengaluru_data = data[data['DISTRICTNAME'] == 'Vijayanagara']

    # Top 15 places with more accidents
    top_units_counts = bengaluru_data['UNITNAME'].value_counts().head(15)
    top_units_labels = top_units_counts.index.tolist()
    top_units_data = top_units_counts.tolist()

    # Types of Roads where Accidents Occur
    road_type_counts = bengaluru_data['Road_Type'].value_counts()
    road_type_labels = road_type_counts.index.tolist()
    road_type_data = road_type_counts.tolist()

    return render_template('./districts/Vijayanagara.html', top_units_labels=top_units_labels,
                            top_units_data=top_units_data,
                            road_type_labels=road_type_labels,
                            road_type_data=road_type_data,
                            accident_counts=accident_counts, suggestions=suggestions)


@app.route('/Yadgir',methods=['GET','POST'])

def Yadgir():
    data = pd.read_csv('main.csv')
    bengaluru_data = data[data['DISTRICTNAME'] == 'Yadgir']

    # Top 15 places with more accidents
    top_units_counts = bengaluru_data['UNITNAME'].value_counts().head(15)
    top_units_labels = top_units_counts.index.tolist()
    top_units_data = top_units_counts.tolist()

    # Types of Roads where Accidents Occur
    road_type_counts = bengaluru_data['Road_Type'].value_counts()
    road_type_labels = road_type_counts.index.tolist()
    road_type_data = road_type_counts.tolist()

    return render_template('./districts/Yadgir.html', top_units_labels=top_units_labels,
                            top_units_data=top_units_data,
                            road_type_labels=road_type_labels,
                            road_type_data=road_type_data,
                             accident_counts=accident_counts, suggestions=suggestions)



data = pd.read_csv('main.csv')
districts = [
    'Bagalkot', 'Bengaluru City', 'Chikkamagaluru', 'Davanagere', 
    'K.G.F', 'Mangaluru City', 'Mysuru City', 'Udupi', 
    'Vijayanagara', 'Yadgir'
]
filtered_data = data[data['DISTRICTNAME'].isin(districts)]

accident_counts = filtered_data['DISTRICTNAME'].value_counts()

suggestions = suggestions = {
    'Bagalkot': [
        "Improve rural road conditions and signage.",
        "Implement educational programs on road safety in rural areas."
    ],
    'Bengaluru City': [
        "Implement stricter speed controls and monitoring.",
        "Enhance traffic management systems in congested areas.",
        "Increase visibility of pedestrian crossings.",
        "Improve street lighting and road signage."
    ],
    'Chikkamagaluru': [
        "Improve road surface conditions and markings.",
        "Enhance safety measures on hilly terrains.",
        "Conduct public awareness campaigns on safe driving practices."
    ],
    'Davanagere': [
        "Improve road infrastructure at accident-prone locations.",
        "Increase enforcement of traffic laws.",
        "Conduct regular vehicle safety inspections."
    ],
    'K.G.F': [
        "Enhance road signage and lighting.",
        "Implement speed control measures in residential areas.",
        "Increase public awareness on traffic safety."
    ],
    'Mangaluru City': [
        "Implement stricter speed controls and monitoring.",
        "Improve visibility of pedestrian crossings.",
        "Enhance road surface conditions and markings."
    ],
    'Mysuru City': [
        "Improve street lighting and road signage.",
        "Increase enforcement of traffic laws.",
        "Implement public awareness campaigns on traffic safety."
    ],
    'Udupi': [
        "Enhance safety measures near schools and colleges.",
        "Implement traffic calming measures in residential areas.",
        "Improve road infrastructure and signage."
    ],
    'Vijayanagara': [
        "Increase visibility of pedestrian crossings.",
        "Improve road surface conditions and markings.",
        "Implement educational programs on road safety."
    ],
    'Yadgir': [
        "Enhance road signage and lighting.",
        "Implement speed control measures in rural areas.",
        "Conduct public awareness campaigns on safe driving."
    ]
}

@app.route('/')
def index():
    user = None
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()

    # Read the data for each analysis
    accident_location_data = pd.read_csv('main.csv')['Accident_Location'].value_counts()
    district_accident_data = pd.read_csv('dis-no.csv')
    road_type_data = pd.read_csv('main.csv')['Road_Type'].value_counts()

    # Generate the chart images as base64 encoded data
    pie_chart_url = generate_pie_chart(accident_location_data)
    line_chart_url = generate_line_chart(district_accident_data)
    bar_chart_url = generate_bar_chart(road_type_data)
    top_units_labels, top_units_data, road_type_labels, road_type_data = generate_chart_data()

    return render_template('index.html', pie_chart_url=pie_chart_url, line_chart_url=line_chart_url, bar_chart_url=bar_chart_url, user=user)



@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # handle request
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')



    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('/')  # Redirect to the dashboard or desired page
        else:
            error = 'Invalid email or password. Please try again.'
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/dashboard')

def dashboard():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('index.html',user=user)
    
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect('/login')



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)