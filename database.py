from firebase import Firebase

config = {
    "apiKey": "AIzaSyBfhQ9VBBnD6pqy-r7-4_JU5FwkpbQCSyM",
    "authDomain": "test-10044.firebaseapp.com",
    "databaseURL": "https://test-10044-default-rtdb.firebaseio.com",
    "projectId": "test-10044",
    "storageBucket": "test-10044.appspot.com",
    "messagingSenderId": "705865082594",
    "appId": "1:705865082594:web:561a0beb6a3ad60315a0bb"
}
firebase = Firebase(config)
db = firebase.database()
auth = firebase.auth()


def insert_regular_visitors(building_name, phone_no, place, visited_flat_no, visitors_id, visitors_name, work):
    data = {
        'building_name': building_name,
        'phone_no': phone_no,
        'place': place,
        'visited_flat_no': visited_flat_no,
        # should be randomly generated but before running the ML program
        'visitors_id': visitors_id,
        'visitors_name': visitors_name,
        'work': work,
    }
    db.child("regularVisitors").child(visitors_id).set(data)


def insert_reports(building_name, checked_by, date, in_time, visitors_id, visitors_name, phone_no, place, temperature, visited_flat_no, work):
    data = {
        "building_name": building_name,
        "checked_by": checked_by,  # will be the watchman id
        "date": date,
        "in_time": in_time,
        "visitors_id": visitors_id,
        "visitors_name": visitors_name,
        "phone_no": phone_no,
        "place": place,
        "temperature": temperature,
        "visited_flat_no": visited_flat_no,
        "work": work
    }

    db.child("reports").child(visitors_id).set(data)


# person_id will be the id token of authentication
def insert_secretary(building_name, email_id, password, person_id, person_name, phone_no):
    data = {
        "building_name": building_name,
        "email_id": email_id,
        "password": password,
        "person_id": person_id,
        "person_name": person_name,
        "phone_no": phone_no,
    }
    db.child("secretary").child(person_id).set(data)


# watchman_id will be the id token of authentication
def insert_watchman(building_name, email_id, password, watchman_id, watchman_name, phone_no, secretary_id):
    data = {
        "building_name": building_name,
        "email_id": email_id,
        "password": password,
        "watchman_id": watchman_id,
        "watchman_name": watchman_name,
        "secretary_id": secretary_id,
        "phone_no": phone_no,
    }
    db.child("watchman").child(watchman_id).set(data)


def display(table_name, id):
    data = db.child(table_name).child(id).get()
    return data.val()


def update(table_name, id, to_update_data, to_update_data_value):
    db.child(table_name).child(id).update(
        {to_update_data: to_update_data_value})


def delete(table_name, id):
    db.child(table_name).child(id).remove()


def sign_in(email, password):
    user = auth.sign_in_with_email_and_password(email, password)
    uid = user['localId']
    if(auth.get_account_info(user['idToken'])['users'][0]['emailVerified'] == False):
        print("Email Not Verified")
        return "Email Not Verified"
    else:
        return uid


def register(email, password):
    user = auth.create_user_with_email_and_password(email, password)
    auth.send_email_verification(user['idToken'])
    uid = user['localId']
    print(uid)
    return uid


def reset(email):
    auth.send_password_reset_email("email")


sign_in("vlakhani28@gmail.com", "helloo")
