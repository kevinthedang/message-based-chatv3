import logging
from constants import *
from datetime import date, datetime
from pymongo import MongoClient
from constants import *

''' Task List for this class: :)
'''

logging.basicConfig(filename='message_chat.log', level=logging.DEBUG, format = LOG_FORMAT)
        
class ChatUser():
    """ class for users of the chat system. Users must be registered 
    """
    def __init__(self, alias: str, user_id = None, email: str = '', blacklist: list = [], removed: bool = False, create_time: datetime = datetime.now(), modify_time: datetime = datetime.now()) -> None:
        self.__alias = alias
        self.__user_id = user_id
        self.__email = email
        self.__create_time = create_time
        self.__modify_time = modify_time
        self.__hash_pass = ''
        self.__blacklist = blacklist
        self.__removed = removed
        if self.__user_id is not None:
            self.__dirty = False
        else:
            self.__dirty = True

    @property
    def alias(self):
        return self.__alias

    @alias.setter
    def alias(self, new_alias):
        if len(new_alias > 2):
            self.__alias = new_alias
            self.dirty = True

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, new_id):
        self.__user_id = new_id
        self.dirty = True

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, new_email):
        self.__email = new_email
        self.dirty = True
    
    @property
    def dirty(self):
        return self.__dirty

    @dirty.setter
    def dirty(self, new_value: bool):
        self.__modify_time = datetime.now()
        self.__dirty = new_value

    @property
    def blacklist(self):
        return self.__blacklist

    @property
    def hash_pass(self):
        return self.__hash_pass

    @hash_pass.setter
    def hash_pass(self, new_password):
        self.__hash_pass = new_password
        self.dirty = True

    @property
    def removed(self):
        return self.__removed

    @removed.setter
    def removed(self, new_value):
        if type(new_value) is bool:
            self.__removed = new_value
            self.dirty = True

    def add_alias_to_blacklist(self, alias) -> bool:
        ''' This method will add a user's alias to the current user's blacklist
            given that the alias is not already in the users blacklist
            NOTE: consider checking if the user exists at the beginning
        '''
        if alias not in self.blacklist:
            self.blacklist.append(alias)
            self.dirty = True
            return True
        return False

    def remove_alias_from_blacklist(self, alias) -> bool:
        ''' This method will remove a user's alias from the current user's blacklist
            given that the alias is in the current user's blacklist
            NOTE: consider checking if the alias exists as a user 
                (may not be necessary since we just want to check if the alias 
                exists in the blacklist, not as a user in the userlist)
        '''
        if alias in self.blacklist:
            self.blacklist.remove(alias)
            self.dirty = True
            return True
        return False

    def to_dict(self):
        return {
                'alias': self.__alias,
                'blacklist': self.blacklist,
                'create_time': self.__create_time,
                'modify_time': self.__modify_time,
                'email': self.__email,
                'removed': self.__removed
        }
        
class UserList():
    """ List of users, inheriting list class
    """
    def __init__(self, list_name: str = DEFAULT_USER_LIST_NAME) -> None:
        self.__user_list = list()
        self.__mongo_client = MongoClient(f'mongodb://{MONGO_DB_HOST}:{MONGO_DB_PORT}/')
        self.__mongo_db = self.__mongo_client.MONGO_DB
        self.__mongo_collection = self.__mongo_db.users  
        if self.__restore() is True:
            logging.info('UserList Document was found in the collection.')
            self.__dirty = False
        else:
            self.__list_name = list_name
            self.__id = None
            self.__create_time = datetime.now()
            self.__modify_time = datetime.now()
            self.__dirty = True

    # This property is just to the the list of users
    @property
    def user_list(self):
        return self.__user_list

    # property returns the id of the userlist
    @property
    def id(self):
        return self.__id

    # This property is to get the list of user_aliases
    @property
    def user_aliases(self):
        return self.get_all_users_aliases

    # property to return the name of the user list
    @property
    def name(self):
        return self.__list_name

    # setter to set the name of the list
    @name.setter
    def name(self, new_list_name):
        if len(new_list_name) > 2:
            self.__list_name = new_list_name
            self.__dirty = True

    # property that checks if the userlist is dirty (needs persistance)
    @property
    def dirty(self):
        return self.__dirty

    # setter that sets the value of the userlist when the userlist is modified outside of userlist
    @dirty.setter
    def dirty(self, new_value):
        if type(new_value) is bool:
            self.__dirty = new_value
            if new_value is True:
                self.__modify_time = datetime.now()

    def __len__(self):
        ''' This method will return the size of the userlist
        '''
        return len(self.user_list)
    
    def register(self, new_alias: str) -> ChatUser:
        """ This method will just return a new ChatUser that will need to be added to the UserList
            This only creates the user, it does not add them to the list of users yet.
            NOTE: we check if the user already exists, if so, don't make another user with that alias
        """
        if (current_user := self.get(new_alias)) is not None:
            return current_user
        if len(new_alias) > 2:
            logging.debug(f'Registered new user with name {new_alias}.')
            user = ChatUser(alias = new_alias)
            self.append(user)
            return user

    def deregister(self, alias_to_remove: str) -> ChatUser:
        ''' This method will return the chat user that was removed from the userlist
            TODO: must remove the user from all members lists (all rooms)
            NOTE: may want to remove this user from all of the users blacklist, 
                or handle it in the restore, making sure that the user exists when updating the blacklist
        '''
        if (user := self.get(alias_to_remove)) is None:
            return user
        user.removed = True
        return user

    def get(self, target_alias: str) -> ChatUser:
        ''' This method will return the user from the user_list
            NOTE: this method will utilize the index to find the user
        '''
        for current_user in self.user_list:
            if target_alias == current_user.alias:
                logging.debug(f'User {target_alias} was found in user list {self.__list_name}.')
                return current_user
        logging.debug(f'User {target_alias} was not found in user list {self.__list_name}.')
        return None

    def get_all_users_aliases(self) -> list:
        ''' This method will just return the list of names as a result.
            NOTE: This list should not be empty as there should at least be an owner to the list
        '''
        logging.debug(f'Attempting to get all user aliases in {self.__list_name}.')
        return [user.alias for user in self.__user_list]

    def append(self, new_user: ChatUser) -> None:
        ''' This method will add the user to the to the list of users
            NOTE: the edge case makes sure that we are not adding nothing into the list
        '''
        if new_user is not None:
            self.__user_list.append(new_user)
            logging.debug(f'Alias {new_user.alias} added to the list of users.')
            self.dirty = True
            self.__persist()

    def __restore(self) -> bool:
        """ First get the document for the queue itself, then get all documents that are not the queue metadata
            NOTE: we should have a list of aliases of the for the members that belong in a certain group chat.
            NOTE: we may not need the user aliases since we just want to restore all of the users          
        """
        logging.info(f'Attempting to restore any user list metadata...')
        user_list_metadata = self.__mongo_collection.find_one( { 'list_name': { '$exists': 'true'} })
        if user_list_metadata is None:
            logging.debug('No user list was not found in the mongo collection.')
            return False
        self.__list_name = user_list_metadata['list_name']
        self.__id = user_list_metadata['_id']
        self.__create_time = user_list_metadata['create_time']
        self.__modify_time = user_list_metadata['modify_time']
        logging.info(f'Attempting to restore users to the {self.__list_name} list.')
        for current_user_metadata in self.__mongo_collection.find({ 'alias': { '$exists': 'true'}}):
            new_chat_user = ChatUser(alias = current_user_metadata['alias'],
                                    user_id = current_user_metadata['_id'],
                                    create_time = current_user_metadata['create_time'],
                                    modify_time = current_user_metadata['modify_time'],
                                    blacklist = current_user_metadata['blacklist'],
                                    email = current_user_metadata['email'],
                                    removed = current_user_metadata['removed'])
            logging.debug(current_user_metadata['alias'] + ' was added to the user list.')
            self.append(new_chat_user)
        logging.info(f'All users in {self.__list_name} added to the user list.')
        return True

    def __persist(self):
        """ First save a document that describes the user list (name of list, create and modify times)
            Second, for each user in the list create and save a document for that user
            NOTE: persisting metadata first then persisting all users in user_list        
        """
        logging.info(f'Attemping to persist user list {self.__list_name}.')
        if self.__mongo_collection.find_one({ 'list_name': self.__list_name}) is None:
            self.__mongo_collection.insert_one({ 'list_name': self.__list_name,
                                                'create_time': self.__create_time,
                                                'modify_time': self.__modify_time})
            logging.debug(f'New user list {self.__list_name} added to the collection.')
        else:
            if self.__dirty == True:
                self.__mongo_collection.replace_one(filter = { 'list_name': self.__list_name},
                                                    replacement = { 'list_name': self.__list_name,
                                                                'create_time': self.__create_time, 
                                                                'modify_time': self.__modify_time},
                                                    upsert = True)
                logging.debug(f'User list {self.__list_name} has been updated in the collection.')
                self.__dirty = False
        for current_user in self.__user_list:
            if current_user.dirty == True:
                if current_user.user_id is None or self.__mongo_collection.find_one({ 'alias': current_user.alias }) is None:
                    serialized = current_user.to_dict()
                    current_user.user_id = self.__mongo_collection.insert_one(serialized)
                else:
                    self.__mongo_collection.replace_one({ '_id': current_user.user_id})
                logging.debug(f'User {current_user.alias} has been added to the collection.')
                current_user.dirty = False
