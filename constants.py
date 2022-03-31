# string constants
MONGO_DB_HOST = '34.94.157.136'
MONGO_DB_USER = 'class'
MONGO_DB_PASS = 'CPSC313'
MONGO_DB_AUTH_SOURCE = 'cpsc313'
MONGO_DB_CLASS_DB = 'cpsc313'
MONGO_DB_CLASS_ROOM_LIST = 'rooms'
MONGO_DB_CLASS_USERS = 'users'
MONGO_DB_AUTH_MECHANISM = 'SCRAM-SHA-256'
DEFAULT_PUBLIC_ROOM = 'general'
DEFAULT_PRIVATE_ROOM = 'kevin_private'
DEFAULT_ROOM_LIST_NAME = 'main'
DEFAULT_USER_LIST_NAME = 'global'
DEFAULT_OWNER_ALIAS = 'kevin'
MONGO_DB_TEST = 'detest'
MONGO_DB = 'cpsc313'

# integer constants
MONGO_DB_PORT = 27017
ROOM_TYPE_PUBLIC = 100
ROOM_TYPE_PRIVATE = 200
GET_ALL_MESSAGES = -1
CHAT_ROOM_INDEX_NOT_FOUND = -1
RIGHT_SIDE_OF_DEQUE = -1
RANGE_STEP = -1
PRIVATE_MESSAGE = 200
PUBLIC_MESSAGE = 100
EMPTY = 0

# possibly unused constants
LOG_FORMAT = '%(levelname)s -- %(message)s'
BYTE_to_STRING = 'utf-8'

# FastAPI Test Constants
STARTUP_URL = 'http://localhost:8000/'
SEND_URL = 'http://localhost:8000/message/'
CREATE_ROOM_URL = 'http://127.0.0.1:8000/room'
GET_USERS_URL = 'http://127.0.0.1:8000/users/'
REGISTER_CLIENT_URL = 'http://127.0.0.1:8000/alias'
GET_MESSAGES_URL = 'http://127.0.0.1:8000/messages/'
STARTUP_TEST_DICTIONARY = { 'from' : 'kevin', 'to' : 'you :)' }
TEST_API_ROOM = 'kevin_api_test_room'
DEFAULT_TEST_API_MESSAGE = 'Kevin has sent this message through FastAPI!'

# User/Room Test Constants
TEST_USER_ALIAS = 'kevin'
TEST_OWNER_ALIAS = 'kevin'
TEST_USER_LIST = 'test_users_kevin'
TEST_LIST_NAME = 'kevin_test_room_list'
DEFAULT_TEST_ROOM = 'kevin_test_room'
DEFAULT_PUBLIC_TEST_MESSAGE = 'Kevin has sent this message publicly.'
DEFAULT_PRIVATE_TEST_MESSAGE = 'Kevin has sent this message privately.'
DEFAULT_FULL_CASE_TEST_MESSAGE = 'This is a full case message by Kevin!'