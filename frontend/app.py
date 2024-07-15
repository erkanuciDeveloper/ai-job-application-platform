import os
import traceback
import jwt
import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from functools import wraps
from bson.objectid import ObjectId
from flask import session

            # Dummy data for job applications and notifications (replace with actual data)
job_applications = [
            {'id': 1, 'title': 'Software Engineer', 'status': 'Pending'},
            {'id': 2, 'title': 'Data Analyst', 'status': 'In Progress'},
            {'id': 3, 'title': 'Web Developer', 'status': 'Completed'}
        ]

notifications = [
            'New job application received',
            'Application status updated'
        ]


# Define the token_required decorator outside the class
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        elif 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = current_app.db['users'].find_one({'_id': ObjectId(data['user_id'])})
            if not current_user:
                return jsonify({'message': 'Token is invalid!'}), 401
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

class JobApplicationPlatform:

    def __init__(self):
        self.setup_flask_app()

    def setup_flask_app(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(current_dir, 'app', 'templates')
        
        self.app = Flask(__name__, template_folder=templates_dir)
        self.app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your actual secret key
        self.app.config['UPLOAD_FOLDER'] = os.path.join(current_dir, 'uploads')
        os.makedirs(self.app.config['UPLOAD_FOLDER'], exist_ok=True)

        global current_app
        current_app = self.app

        self.setup_routes()
        self.setup_mongodb()
        self.setup_bcrypt()

    def setup_routes(self):
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/signup', 'signup_page', self.signup_page)
        self.app.add_url_rule('/login', 'login_page', self.login_page)
        self.app.add_url_rule('/login', 'login', self.login, methods=['POST'])
        self.app.add_url_rule('/signup', 'signup', self.signup, methods=['POST'])
        self.app.add_url_rule('/profile', 'profile_page', self.profile_page) # for GET
        self.app.add_url_rule('/profile', 'profilepage', self.profilepage, methods=['POST'])
        self.app.add_url_rule('/dashboard', 'dashboard', self.dashboard)
        self.app.add_url_rule('/job_applications', 'get_job_applications', self.get_job_applications)
        self.app.add_url_rule('/notifications', 'get_notifications', self.get_notifications)
        self.app.add_url_rule('/protected', 'protected', token_required(self.protected))

      

        


    def setup_mongodb(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['job_application_platform']
        self.users_collection = self.db['users']

    def setup_bcrypt(self):
        self.bcrypt = Bcrypt(self.app)

    def index(self):
        return render_template('index.html')

    def signup_page(self):
        return render_template('signup.html')

    def login_page(self):
        token = session.get('token')
        # if token:
        #     token = request.headers['x-access-token']
            
            
        #     return redirect(url_for('profile_page.html'))
        # else:
        #     return render_template('login.html')
        return render_template('login.html')


    def profile_page(self):
        return render_template('profile.html')
    

    
# Other methods...

    def dashboard(self):
        # You can implement logic here to retrieve data for the dashboard
        # For now, let's assume you have some sample data
        # You can replace this with your actual logic to fetch dashboard data
        dashboard_data = {
            'total_job_applications': 50,
            'pending_applications': 20,
            'approved_applications': 15,
            'rejected_applications': 15,
            'total_notifications': 10
        }
        return render_template('dashboard.html', dashboard_data=dashboard_data)

    def get_job_applications(self):
        # You can implement logic here to retrieve job applications from your database
        # For now, let's assume you have some sample data
        job_applications = [
            {'title': 'Software Engineer', 'status': 'Pending'},
            {'title': 'Data Scientist', 'status': 'Approved'},
            {'title': 'UI/UX Designer', 'status': 'Rejected'}
            # Add more job application data as needed
        ]
        return render_template('job_applications.html', job_applications=job_applications)

    def get_notifications(self):
        # You can implement logic here to retrieve notifications from your database
        # For now, let's assume you have some sample data
        notifications = [
            {'message': 'New job application received', 'timestamp': '2024-06-05 10:00:00'},
            {'message': 'Application status updated', 'timestamp': '2024-06-04 15:30:00'},
            # Add more notification data as needed
        ]
        return render_template('notifications.html', notifications=notifications)


    def signup(self):
        try:
            data = request.json
            username = data['username']
            email = data['email']
            password = data['password']
            
            hashed_password = self.bcrypt.generate_password_hash(password).decode('utf-8')
            
            user_data = {
                'username': username,
                'email': email,
                'password': hashed_password
            }
            
            result = self.users_collection.insert_one(user_data)
            
            if result.inserted_id:
                return redirect(url_for('login_page'))
            else:
                return 'Error occurred while signing up', 500
        except Exception as e:
            traceback.print_exc()
            return f'An error occurred while signing up: {str(e)}', 500
   
    def login(self):
        try:
            if not request.is_json:
                return jsonify({'message': 'Request must be JSON.'}), 400
            
            data = request.json
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return jsonify({'message': 'Email and password are required fields.'}), 400
            
            user = self.users_collection.find_one({'email': email})
            
            if user and self.bcrypt.check_password_hash(user['password'], password):
                token = jwt.encode({
                    'user_id': str(user['_id']),
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
                }, self.app.config['SECRET_KEY'], algorithm="HS256")

                session['token'] = token
                user_data = {
                    'username': user['username'],
                    'email': user['email']
                }
                
                return jsonify({'token': token, 'user': user_data, 'redirect': '/profile'})
            else:
                return jsonify({'message': 'Wrong email or password. Try again or create an account.'}), 401
        except Exception as e:
            traceback.print_exc()
            return jsonify({'message': f'An error occurred while logging in: {str(e)}'}), 500

    @token_required
    def profilepage(self, current_user):
        if request.method == 'POST':
            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']
                    
            if token:
                try:
                    data = jwt.decode(token, self.app.config['SECRET_KEY'], algorithms=["HS256"])
                    current_user = self.users_collection.find_one({'_id': ObjectId(data['user_id'])})
                except Exception as e:
                    return jsonify({'message': 'Token is invalid!'}), 401
            if current_user:
                cv = request.files['cv']
                if cv:
                    cv_filename = os.path.join(self.app.config['UPLOAD_FOLDER'], cv.filename)
                    cv.save(cv_filename)
                    self.users_collection.update_one(
                        {'_id': current_user['_id']},
                        {'$set': {'cv_path': cv_filename}}
                    )
                    return jsonify({'message': 'CV uploaded successfully'}), 200
                else:
                    return jsonify({'message': 'No file uploaded'}), 400
            else:
                return jsonify({'message': 'Token is missing!'}), 401

    def protected(self, current_user):
        return f'Hello {current_user["username"]}, you have accessed a protected route!'

    def run(self):
        self.app.run(debug=True, host='0.0.0.0')

if __name__ == "__main__":
    job_app_platform = JobApplicationPlatform()
    job_app_platform.run()
