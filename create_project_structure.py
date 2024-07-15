import os

def create_directory_structure(root_dir):
    directories = [
        'backend',
        'ai_ml_service',
        'frontend/app/static',
        'frontend/app/templates',
        'frontend/src/components/Auth',
        'frontend/src/components/Profile',
        'frontend/src/components/Dashboard',
        'frontend/src/components/common',
        'frontend/src/pages',
        'frontend/src/services',
        'frontend/src/store/actions',
        'frontend/src/store/reducers'
    ]

    for directory in directories:
        os.makedirs(os.path.join(root_dir, directory), exist_ok=True)

    files = [
        'backend/Dockerfile',
        'backend/package.json',
        'backend/server.js',
        'ai_ml_service/Dockerfile',
        'ai_ml_service/main.py',
        'ai_ml_service/requirements.txt',
        'frontend/Dockerfile',
        'frontend/app.py',  # Added this file
        'frontend/package.json',
        'frontend/src/App.js',
        'frontend/src/index.js',
        'frontend/src/routes.js',
        'frontend/src/index.html',
        'frontend/app/__init__.py',
        'frontend/app/routes.py',
        'frontend/app/views.py',
        'frontend/src/components/Auth/Login.js',
        'frontend/src/components/Auth/Register.js',
        'frontend/src/components/Profile/ProfileForm.js',
        'frontend/src/components/Dashboard/Dashboard.js',
        'frontend/src/components/Dashboard/JobCard.js',
        'frontend/src/components/Dashboard/Notification.js',
        'frontend/src/components/common/Header.js',
        'frontend/src/components/common/Footer.js',
        'frontend/src/pages/Home.js',
        'frontend/src/pages/Login.js',
        'frontend/src/pages/Register.js',
        'frontend/src/pages/Profile.js',
        'frontend/src/pages/Dashboard.js',
        'frontend/src/services/authService.js',
        'frontend/src/services/profileService.js',
        'frontend/src/services/jobService.js',
        'frontend/src/store/actions/authActions.js',
        'frontend/src/store/actions/profileActions.js',
        'frontend/src/store/actions/jobActions.js',
        'frontend/src/store/reducers/authReducer.js',
        'frontend/src/store/reducers/profileReducer.js',
        'frontend/src/store/reducers/jobReducer.js',
        'frontend/src/store/store.js',
        'docker-compose.yml',
        'README.md'
    ]

    for filepath in files:
        with open(os.path.join(root_dir, filepath), 'w') as file:
            file.write('')

if __name__ == "__main__":
    project_root = "C:/Workspace/job-application-platform"
    create_directory_structure(project_root)
    print("Project structure and files created successfully.")
