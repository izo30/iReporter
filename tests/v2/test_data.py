signup_url = 'api/v2/auth/signup'
login_url = 'api/v2/auth/login'
incident_url = "/api/v2/incidents"

user1 = dict(
    first_name = 'triza',
    last_name = 'wambui',
    email = 'triza@gmail.com',
    phone = '0736547657', 
    username = 'triza',
    password = 'F31+25e9',
    role = 'user'
)

user2 = dict(
    first_name = 'harry',
    last_name = 'potter',
    email = 'harry@gmail.com',
    phone = '0736547657', 
    username = 'harry',
    password = 'F31+25e9',
    role = 'user'
)

user3 = dict(
    first_name = 'mercy',
    last_name = 'wanjiru',
    email = 'mercy@gmail.com',
    phone = '0736547657', 
    username = 'mercy',
    password = '1234567',
    role = 'user'
)

user4 = dict(
    first_name = 'john',
    last_name = 'doe',
    email = 'john.com',
    phone = '0736547657', 
    username = 'john',
    password = 'F31+25e9',
    role = 'user'
)

user5 = dict(
    first_name = 'hamani',
    last_name = 'grain',
    email = 'hamani@gmail.com',
    phone = '0736547657', 
    username = 'hamani',
    password = 'F31+25e9',
    role = 'user'
)

user5_login = dict(
    email = 'hamani@gmail.com',
    password = 'F31+25e9',
)

admin_login = dict(
    email = 'isaacwangethi30@gmail.com',
    password = 'F31+25e9',
)

encode_token_data = dict(
    user_id = 'aa520a77-a9a2-461c-9efa-169bb698391c',
    email = 'brian@gmail.com',
    role = 'user'
)

incident1 = dict(
    type = 'intervention',
    latitude = '4.58',
    longitude = '9.45',
    images = 'image.jpg',
    videos = 'video.mp4',
    comments = 'government offices around kahawa area need renovation'
) 

incident2 = dict(
    type = 'red flag',
    latitude = '8.58',
    longitude = '12.45',
    images = 'image.jpg',
    videos = 'video.mp4',
    comments = 'huduma center officer demanded for an extra fee to provide services'
)

incident3 = dict(
    type = 'red flag',
    latitude = '6.58',
    longitude = '9.45',
    images = 'image.jpg',
    videos = 'video.mp4',
    comments = 'the police was given a bribe by the matatu conductor'
)

incident4 = dict(
    type = 'intervention',
    latitude = '6.58',
    longitude = '9.45',
    images = 'image.jpg',
    videos = 'video.mp4',
    comments = 'kahawa west road needs maintenance'
) 

admin_edited_status = {
    "status": "under investigation"
}

edited_comment = {
    "comments": "government offices around kahawa area need renovation"
}

edited_location = {
    "latitude": "0.475",
    "longitude": "5.348"
}