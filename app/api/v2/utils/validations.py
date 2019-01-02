import re
from flask_restplus import reqparse

class Validations():

    def __init__(self):
        pass

    def add_arguments(self, parser, fields):
        for field in fields:
            parser.add_argument(field, help = 'Field {} cannot be blank.'.format(field), required = True)
    
    def validate_password(self, password):
        if re.match(r"(((?=.*[a-z])(?=.*[A-Z]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[A-Z])(?=.*[0-9])))(?=.{8,})", password):
            return True
        return False

    def validate_email(self, email):
        if re.match(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return True
        return False

    def validate_name(self, name):
        if re.match(r"(^[a-zA-Z]+$)", name):
            return True
        return False

    def check_if_empty(self, fields):
        is_empty = False
        is_empty_message = {}
        for key, value in fields.items():
            if not value:
                is_empty = True
                is_empty_message[key] = "{} should not be empty".format(key)
        if is_empty:
            return is_empty_message
        return is_empty

    def check_if_role(self, role):
        if role == "admin":
            return True
        elif role == "user":
            return True
        else:
            return False

    def token_present(self, token):
        if token:
            return True

    def check_if_admin(self, role):
        if role == "admin":
            return True

    def check_if_user(self, role):
        if role == "user":
            return True

    def check_token_error(self, message):
        if message == "Signature expired. Please log in again.":
            return message
        if message == "Invalid token. Please log in again.":
            return message

    def validate_user_data(self, first_name, last_name, email, phone, username, password, role):

        error_response = {}
        error = False

        user = dict(
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone = phone,
            username = username,
            password = password,
            role = role
        )

        is_empty = self.check_if_empty(user)
        if is_empty:
            return dict(error = is_empty)
        if not self.validate_name(first_name):
            error = True
            error_response['first_name'] = "First name should contain letters only"
        if not self.validate_name(last_name):
            error = True
            error_response['last_name'] = "Last name should contain letters only"
        if not self.validate_email(email):
            error = True
            error_response['email'] = "Invalid email"
        if not re.match(r"^([\s\d]+)$", phone):
            error = True
            error_response['phone'] = "Invalid phone number"
        if not re.match(r"[a-z A-Z0-9\_\"]+$", username):
            error = True
            error_response['username'] = "Username should contain only numbers, letters and underscore"
        if not self.validate_password(password):
            error = True
            error_response['password'] = "The password should contain a small and a capital letter, a number and a special character"
        if not self.check_if_role(role):
            error = True
            error_response['role'] = "Role should be admin or user"

        if error:
            print ("ERROR : {}" .format(error_response))
            error_message = dict( error = error_response )
            return error_message

    def check_if_status(self, status):
        if status == "draft": return True
        elif status == "under investigation": return True
        elif status == "resolved": return True
        elif status == "rejected": return True
        else: return False

    def check_if_type(self, incident_type):
        if incident_type == "intervention": return True
        elif incident_type == "red flag": return True
        elif incident_type == "edit": return True
        else: return False

    def validate_location(self, location):
        for value in location:
            if re.match(r"^\d+?\.\d+?$", value): return True
            else: return False

    def validate_comments(self, comment):
        if re.match(r"^[a-zA-Z\d\-_\s,.;:\"']+$", comment):
            return True
        return False

    def validate_incident_data(self, latitude, longitude, images, videos, comments, type="edit"):

        error_response = {}
        error = False

        incident = dict(
            latitude = latitude,
            longitude = longitude,
            images = images,
            videos = videos,
            comments = comments,
            type = type
        )

        is_empty = self.check_if_empty(incident)
        if is_empty:
            return dict(error = is_empty)
        if not Validations().check_if_type(type):
            error = True
            error_response['type'] = "Type should be intervention or red flag"
        if not Validations().validate_location([latitude, longitude]):
            error = True
            error_response['location'] = "Latitude and longitude should be a float"
        if not re.match(r"([a-zA-Z0-9\s_\\.\-\(\):])+(.jpg|.png|.jpeg|.gif)$", images):
            error = True
            error_response['image'] = "Invalid image format"
        if not re.match(r"([a-zA-Z0-9\s_\\.\-\(\):])+(.mp4|.mov|.mkv)$", videos):
            error = True
            error_response['videos'] = "Invalid video format"
        if not self.validate_comments(comments):
            error = True
            error_response['comments'] = "Comments should contain alphanumeric plus ,.;:\"' only"

        if error:
            error_message = dict( error = error_response )
            return error_message