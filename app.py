from flask import Flask, request, jsonify

app = Flask(__name__)

userList = [{
    "id": 1,
    "name": "Mohammad Amin",
    "email": "helloamin.com@gmail.com",
    "password": "123456",
    "location": "tabriz",
}]

#? get all of users
@app.route("/users", methods=['GET'])
def get_users():
    return jsonify(userList)

#? login user
@app.route("/login", methods=['POST'])
def login_user():
    #* Get the JSON data from the request
    client_data = request.get_json()

    try:
        #* Check if the request data is valid
        user = next((u for u in userList if u["email"] == client_data["email"]), None)
        
        #* If the user is found
        if user:
            #* Check if the password matches
            if user["password"] == client_data["password"]:
                return jsonify({ "user": user}), 200
            
            #* If the password does not match
            else:
                return jsonify({ "message": "wrong password!"}), 401
    
        #* If the user is not found
        else :
            return jsonify({ "message": "user not found!"}), 404

    #* Handle any unexpected errors    
    except Exception as e:
        return jsonify({ "message": str(e)}), 500

#? register user
@app.route("/register", methods=['POST'])
def register_user():
    #* Get the JSON data from the request
    client_data = request.get_json()

    try:
        #* Check if the request data is valid
        user = next((u for u in userList if u["email"] == client_data["email"]), None)

        #* If the user already exists
        if user:
            return jsonify({ "message": "User already exists!"}), 409
    
        #* If the user does not exist, create a new user
        else:
            new_user = {
                "id": len(userList) + 1,
                "name": client_data["name"],
                "email": client_data["email"],
                "password": client_data["password"],
                "location": client_data["location"],
            }
            userList.append(new_user)
            return jsonify({"user": new_user}), 201

    #* Handle any unexpected errors
    except Exception as e:
        return jsonify({ "message": str(e)}), 500

#? delete user
@app.route("/delete", methods=['POST'])
def delete_user():
    #* Get the JSON data from the request
    client_data = request.get_json()

    try:
        #* Check if the request data is valid
        user = next((u for u in userList if u["email"] == client_data["email"]), None)

        #* If the user is found, delete it
        if user:
            userList.remove(user)
            return jsonify({ "message": "User deleted successfully!"}), 200
        
        #* If the user is not found
        else:
            return jsonify({ "message": "User not found!"}), 404

    #* Handle any unexpected errors
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
#? update user
@app.route("/update", methods=['POST'])
def update_user():
    #* Get the JSON data from the request
    client_data = request.get_json()

    try:
        #* Check if the request data is valid
        user = next((u for u in userList if u["email"] == client_data["email"]), None)

        #* If the user is found, update it
        if user:
            user["name"] = client_data.get("name", user["name"])
            user["password"] = client_data.get("password", user["password"])
            return jsonify({"user": user}), 200
        
        #* If the user is not found
        else:
            return jsonify({ "message": "User not found!"}), 404

    #* Handle any unexpected errors
    except Exception as e:
        return jsonify({ "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
