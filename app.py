from flask import Flask
from flask import session,redirect,render_template
from flask.globals import request
from flask_pymongo import PyMongo
from datetime import datetime

app=Flask(__name__)

app.secret_key="communication_key" #Communication ke which is require to be set to use sessions

MONGO_URI="mongodb://127.0.0.1:27017/valet"
mongodb_client=PyMongo(app,MONGO_URI)#General connectors
dbo=mongodb_client.db

@app.route("/",methods=["GET","POST"])
def signup_home():
    return render_template("signup.html")

# Authentication starts
@app.route("/signup",methods=["GET","POST"])

def signup_func():
    username=request.form.get("username")
    email=request.form.get("email")  #check for format in front_end
    phone=request.form.get("phone") #check for format in front_end 
    password=request.form.get("password") #check for format in front_end
    confirm_password=request.form.get("confirm_password")

    check_pass=check_password(password,confirm_password)
    check_db_entry=check_database(email)
    if check_db_entry==True and check_pass==True:
        dbo.users.insert({
            "email":email,
            "username":username,
            "phone":phone,
            "password":password
        })
        return render_template("login.html")

    else:
        return "duplicate entry exists or password and confirm_password are mismatched"


def check_database(email):
    entry=dbo.users.find_one({"email":email})
    print(entry)
    if entry is None:
        return True
    else:
        return False

def check_password(password,confirm_password):
    if(password==confirm_password):
        return True
    else:
        return False 

@app.route("/forget_password",methods=["GET","POST"])
def forget_password_function():
    email=request.json["email"]
    found_flag=dbo.users.find_one({"email":email}) #find_one always returns a dictionary , find returns a pymongo cursor object
    
    if found_flag is None:
        return "No email found"
    else:
        return "This page of sending a temp password is under development"
        #email the user a temporary password and then allow change in password

@app.route("/login",methods=["GET","POST"])
def login_func():
    email=request.json["email"]#check format in front end
    password=request.json["password"]#check format in front end 
    user_found=dbo.users.find_one({"email":email,"password":password})
    if user_found is None:
        return "Authentication Failed"
    else:
        session["username"]=email
        session["password"]=password
        return render_template("home.html")

@app.route("/home")

def home():
    if session.get("username",None) is None and session.get("password",None) is None:


        return redirect("/login")
    else:
        return "<h1>Welcome home champ</h1>"

@app.route("/logout",methods=["GET","POST"])

def logout():
    session.pop("username")
    session.pop("password")
    return "You are logged out successfully and your session has been completely taken off"

#Authentication ends ( Note that Authentication applies for restaurant owners)

@app.route("/register_a_car",methods=["GET","POST"])

def register():
    if session.get("username") is None:
        return "You are not logged in "
    else:
        pass
    car_number=request.json["car_number"]
    dbo.points.insert_one({"car_number":car_number,"points":0})
    return "Entry was registered successfully"

@app.route("/main_car_enters",methods=["GET","POST"])
def car_enters():
    car_number=request.json["car_number"]
    found_flag=dbo.points.find_one({"car_number":car_number})
    if (found_flag):
        # points=dbo.points.find_one({"car_number":car_number},{"points":1})
        # print(points['points'])
        pass
    else:
        return ("The car was not registered , please intimate the driver for a Subscription card")
    day = datetime.today().strftime("%a")
    if day == "Sun" or day == "Sat" :
       dbo.points.update({"car_number":car_number})
       return("succesfully updated")
    else:
        dbo.points.update({"car_number":car_number},{"$inc":{"points":50}})
        return("succesfully updated")
    
        

        


#Routes for functionality 





    





if __name__ == "__main__":
    app.run(debug=True)


    
        

