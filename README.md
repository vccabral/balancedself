# balancedself
A repo for http://balancedself.herokuapp.com/

The website is for creating balanced meals.

# Set Up Instructions
1) Install git from github.com
2) Clone the balancedself repo and cd into repo
```
git clone https://github.com/vccabral/balancedself.git
cd balancedself
```
3) If you don't already have Virtual Environment on your machine, get it
```
pip install virtualenv
```
4) Create a virtual environment
```
virtualenv venv
```
5) Activate the newly created virtual environment
```
source venv/bin/activate
```
6) Install Python dependencies
```
pip install -r requirements.txt
```
7) Migrate Django models
```
python manage.py migrate
```
8) Run it locally
```
python manage.py runserver 0.0.0.0:3000
```
9) Open a browser and point it to 0.0.0.0:3000
```
export FB_APP=[facebook app id]
export FB_SECRET=[facebook secret id]
```
10) To allow facebook authenication, setup a facebook app or use our facebook app id and secret.

