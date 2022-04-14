import unittest
from unittest import TestCase
from constants import *
from users import *

class UserTest(unittest.TestCase):
    """ This test environment will test the functionality of UserList using a different UserList
        TODO: make tests in decending order
    """
    def setUp(self) -> None:
        ''' This setup test method will instantiate the UserList for the name of the user list.
            NOTE: When the test runs, since there will be persistence of usernames, we may want to reinitialize an empty list to test functionality
        '''
        self.__user_list = UserList(TEST_USER_LIST)

    def test_adding(self):
        ''' This test should do the following:
                - register a new user to the DB, as long as they do not exist
                - add the user to the list
                - the UserList will persist and restore every time when adding a new user
            TODO: make this instance unique
        '''
        new_chat_user = self.__user_list.register(new_alias = TEST_USER_ALIAS)
        if new_chat_user is None:
            self.__user_list.remove_all()
            new_chat_user = self.__user_list.register(new_alias = TEST_USER_ALIAS)
        self.assertTrue(self.__user_list.append(new_user = new_chat_user))

    def test_getting(self):
        ''' This test should make sure that the usernames in the user list above are found and persisted
                from the previous test 
            NOTE: this test can add/register a user to the list and see if they can get the user_alias from the list
        '''
        test_user = self.__user_list.get(target_alias = TEST_USER_ALIAS)
        self.assertEqual(TEST_USER_ALIAS, test_user.alias)