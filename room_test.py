import unittest
from datetime import datetime
from unittest import TestCase
from constants import *
from room import ChatRoom, MessageProperties, RoomList
from users import *

class RoomTest(unittest.TestCase):
    """ This test environment will test the functionality of the room file
        TODO: make user testing file first
    """
    def setUp(self) -> None:
        ''' This setup method will just declare the public and private room to test on.
            TODO: set up the room list class here
        '''
        self.users = UserList()
        self.room_list = RoomList()
        self.room_public = self.room_list.get(DEFAULT_PUBLIC_ROOM)
        if self.room_public is None:
            self.room_public = self.room_list.create(room_name = DEFAULT_PUBLIC_ROOM, owner_alias = 'testing', room_type = ROOM_TYPE_PUBLIC)
            self.room_list.add(self.room_public)
        self.room_private = self.room_list.get(DEFAULT_PRIVATE_ROOM)
        if self.room_private is None:
            self.room_private = self.room_list.create(room_name = DEFAULT_PRIVATE_ROOM, owner_alias = 'testing', room_type = ROOM_TYPE_PRIVATE)
            self.room_list.add(self.room_private)

    def test_send(self, private_message: str = DEFAULT_PRIVATE_TEST_MESSAGE, public_message: str = DEFAULT_PUBLIC_TEST_MESSAGE) -> bool:
        """ Testing the send message functionality
            NOTE: These assertions should come back as true from the method calling
                    A true means that the message was sent to Rabbit
            TODO: just send a message to the deque and make sure it gets persisted
        """
        self.assertTrue(self.room_private.send_message(message = private_message,
                                    from_alias = TEST_OWNER_ALIAS,
                                    mess_props = MessageProperties(room_name = DEFAULT_TEST_ROOM, 
                                                                to_user = TEST_OWNER_ALIAS, 
                                                                from_user = TEST_OWNER_ALIAS, 
                                                                mess_type = PRIVATE_MESSAGE)))
        self.assertTrue(self.room_public.send_message(message = public_message,
                                    from_alias = TEST_OWNER_ALIAS,
                                    mess_props = MessageProperties(room_name = DEFAULT_TEST_ROOM, 
                                                                to_user = TEST_OWNER_ALIAS, 
                                                                from_user = TEST_OWNER_ALIAS, 
                                                                mess_type = PUBLIC_MESSAGE)))

    def test_get(self) -> list:
        """ Testing the get messages functionality
            NOTE: Should make sure that the sequence of the messages are correct
            TODO: we want to reload and restore the messages in the test chat and get the message
        """
        tuple_of_messages = self.__chat_room.get_messages(user_alias = TEST_OWNER_ALIAS)
        self.assertEqual(tuple_of_messages[2], self.__chat_room.num_messages)
        self.assertIn(DEFAULT_PRIVATE_TEST_MESSAGE, tuple_of_messages[0])
        self.assertIn(DEFAULT_PUBLIC_TEST_MESSAGE, tuple_of_messages[0])

    def test_full(self):
        """ Doing both and make sure that what we sent is in what we get back
            TODO: we want to test the send and receieve
        """
        self.assertTrue(self.__chat_room.send_message(message = DEFAULT_FULL_CASE_TEST_MESSAGE,
                                    from_alias = TEST_OWNER_ALIAS,
                                    mess_props = MessageProperties(room_name = DEFAULT_TEST_ROOM, 
                                                                to_user = TEST_OWNER_ALIAS, 
                                                                from_user = TEST_OWNER_ALIAS, 
                                                                mess_type = PRIVATE_MESSAGE)))
        tuple_of_messages = self.__chat_room.get_messages(user_alias = TEST_OWNER_ALIAS)
        self.assertEqual(tuple_of_messages[2], self.__chat_room.num_messages)
        self.assertIn(DEFAULT_FULL_CASE_TEST_MESSAGE, tuple_of_messages[0])