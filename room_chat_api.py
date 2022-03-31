import socket
import logging
import json
from fastapi import FastAPI, Request, status, Form
from fastapi.responses import JSONResponse, ORJSONResponse, Response
from fastapi.templating import Jinja2Templates
from room import *
from constants import *
from users import *

MY_IPADDRESS = ""

''' Reasons for global variables:
        - The first is the documented way to deal with running the app in uvicorn
        - The second one handles the RoomList to access the rooms from MongoDB
        - The third one handles the users in the UserList from MongoDB
'''
logging.basicConfig(filename='message_chat.log', level=logging.INFO, format = LOG_FORMAT)
app = FastAPI()
room_list = RoomList()
users = UserList()
templates = Jinja2Templates(directory="")

@app.get("/")
async def index():
    """ Default page
        NOTE: when the user accesses the main page, they will get the following JSON response (dictionary)
    """
    return { 'message' : { 'from' : 'kevin', 'to' : 'you :)' }}

@app.get("/page/send", status_code=200)
async def send_form(request: Request):
    """ HTML GET page form sending a message
    """
    pass

@app.post("/page/send", status_code=201)
async def get_form(request: Request, room_choice: str = Form(...), message: str = Form(...), alias: str = Form(...)):
    """ HTML POST page for sending a message
    """
    pass

@app.get("/page/messages", status_code=200)
async def form_messages(request: Request, room_name: str = DEFAULT_PUBLIC_ROOM):
    """ HTML GET page for seeing messages
    """
    pass

@app.post("/page/messages", status_code=201)
async def form_messages(request: Request, room_name: str = Form(...)):
    """ HTML POST page for seeing messages in a different room or different quantities
    """
    pass

@app.get("/messages/", status_code = 200)
async def get_messages(alias: str, room_name: str, messages_to_get: int = GET_ALL_MESSAGES):
    """ API for getting messages from a room
        NOTE: this user must be a valid member of the room to access the messages to the room.
    """
    logging.info(f'Attempting to get messages from {room_name} room...')
    if room_name not in room_list.get(room_name = room_name):
        logging.debug(f'Room {room_name} was not found in the list of rooms.')
        return JSONResponse(content = { 'message': f'Room {room_name} was not found in the list of rooms.'}, status_code = 400)
    room_requested = room_list.get(room_name = room_name)
    if alias not in users.get_all_users_aliases() or (alias not in room_requested.member_list and room_requested.room_type is ROOM_TYPE_PRIVATE):
        logging.warning(f'User {alias} does not exist or they are not a member of the room.')
        return JSONResponse(content = { 'message': f'User {alias} does not exist or they are not a member of the room.'}, status_code = 400)
    try:
        messages_in_room = room_requested.get_messages(user_alias = alias, num_messages = messages_to_get)
        if messages_in_room[2] is EMPTY:
            logging.debug(f'No messages found in room {room_name}.')
            return JSONResponse(content = { 'message': 
                                        { 'data': {
                                            'message_texts': messages_in_room[0],
                                            'message_objects': messages_in_room[1],
                                            'num_messages': messages_in_room[2]
                                        }}})
        else:
            logging.debug(f'{messages_in_room[2]} messages were found in {room_name} for user {alias}.')
            return JSONResponse(content = { 'message': 
                                        { 'data': {
                                            'message_texts': messages_in_room[0],
                                            'message_objects': messages_in_room[1],
                                            'num_messages': messages_in_room[2]
                                        }}})
    except:
        logging.error(f'Unknown Error obtaining the messages in room {room_name} for user {alias}.')
        return JSONResponse(content = { 'message': f'Unknown Error obtaining the messages in room {room_name} for user {alias}.' }, status_code = 400)

@app.get("/users/", status_code = 200)
async def get_users():
    """ API for getting users
        NOTE: this will just access the userList from the call above and attempt to get the users, most likely just aliases.
    """
    logging.info('Attempting to get all of the users from the user list...')
    try:
        if len(users.get_all_users_aliases()) is EMPTY:
            logging.debug('No users were found in the user list.')
            return JSONResponse(content = 'No users were found in the user list.', status_code = 400)
        else:
            logging.debug('A list of users was given to the client user')
            return JSONResponse(content = { 'message': { 'list_of_users': users.get_all_users_aliases() }}, status_code = 200)
    except:
        logging.error('Unknown Error obtaining all the users in the user list.')
        return JSONResponse(content = { 'message': 'Unknown Error obtaining all the users in the user list.' }, status_code = 400)

@app.post("/alias", status_code = 201)
async def register_client(client_alias: str):
    """ API for adding a user alias
        TODO: access the UserList var above and attempt to register and add the user to the UserList
    """
    logging.info(f'Attempting to register {client_alias} as a user...')
    try:
        if users.append(users.register(new_alias = client_alias)) is True:
            logging.debug(f'User {client_alias} was successfully registered as a new user to the user list.')
            return JSONResponse(content = { 'message': f'{client_alias} was successfully added to the list of users.' }, status_code = 201)
        else:
            logging.debug(f'{client_alias} is already registered as a user.')
            return JSONResponse(content = { 'message': f'User {client_alias} already exists in the list of users.' }, status_code = 403)
    except:
        logging.error(f'Unknown Error registering a user with the name {client_alias}.')
        return JSONResponse(content = { 'message': f'Unknown Error registering a user with the name {client_alias}.' }, status_code = 400)

@app.post("/room", status_code = 201)
async def create_room(room_name: str, owner_alias: str, room_type: int = ROOM_TYPE_PRIVATE):
    """ API for creating a room
        NOTE: there are edge cases to make sure no duplicates of rooms
    """
    logging.info(f'{owner_alias} is attempting to create a room with the name {room_name} to the room list...')
    if owner_alias not in users.get_all_users_aliases():
        logging.debug(f'{owner_alias} was not a valid user alias in the UserList.')
        return JSONResponse(content = { 'message': 'Users not found in UserList.' }, status_code = 412)
    try:
        new_chat_room = room_list.create(room_name = room_name, owner_alias = owner_alias, room_type = room_type)
        if new_chat_room is None and room_list.add(new_room = new_chat_room) is None:
            logging.debug(f'"{room_name}" room already exists in the list of rooms.')
            return JSONResponse(content = { 'message': f'"{room_name}" room already exists in the list of rooms.' }, status_code = 409)
        else:
            return JSONResponse(content = { 'message': f'"{room_name}" room has been successfully added to the list of rooms.' }, status_code = 201)
    except:
        logging.error(f'Unknown Error creating a room with name {room_name} by {owner_alias}.')
        return JSONResponse(content = { 'message': f'Unknown Error creating a room with name {room_name} by {owner_alias}.'}, status_code = 400)

@app.post("/message/", status_code = 201)
async def send_message(room_name: str, message: str, from_alias: str, to_alias: str):
    """ API for sending a message, for a particular room
        TODO: this may want to access the send_message feature from a chatroom
    """
    logging.info(f'Attempting to send "{message}" to {to_alias} from {from_alias}...')
    if from_alias not in users.get_all_users_aliases() and to_alias not in users.get_all_users_aliases():
        logging.debug(f'{from_alias} or {to_alias} was not a valid user alias in the UserList.')
        return JSONResponse(content = { 'message': 'Users not found in UserList.'}, status_code = 412)
    if room_list.get(room_name = room_name) is None:
        logging.debug(f'ChatRoom {room_name} does not exists in the list of rooms.')
        return JSONResponse(content = { 'message': f'{room_name} room was not found in room list.'}, status_code = 409)
    requested_chat_room = room_list.get(room_name = room_name)
    try:
        request_status = requested_chat_room.send_message(message = message, 
                                                        from_alias = from_alias, 
                                                        mess_props = MessageProperties(room_name = room_name,
                                                                                    to_user = to_alias,
                                                                                    from_user = from_alias,
                                                                                    mess_type = PRIVATE_MESSAGE))
        if request_status is True:
            logging.debug(f'"{message}" was successfully sent to {to_alias} from {from_alias}.')
            return JSONResponse(content = { 'message': f'{message} was successfully sent to {to_alias}.'}, status_code = 201)
        else:
            logging.warning(f'User {from_alias} attempted to send a message to a room they are not a member of!')
            return JSONResponse(content = { 'message': f'{message} was not sent successfully to {to_alias}.'}, status_code = 412)
    except:
        logging.error(f'Unknown Error when sending {message} to {to_alias}.')
        return JSONResponse(content = { 'message': f'Unknown Error sending {message} to {to_alias}.'}, status_code = 400)

def main():
    ''' Main method to get the current user alias
    '''
    MY_IPADDRESS = socket.gethostbyname(socket.gethostname())
    MY_NAME = input("Please enter your name: ")

if __name__ == "__main__":
    main()