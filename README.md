# Message Chat Using MongoDB
This implementation of a message chat will utilize MongoDB and FastAPI while implementing new methods (i.e. like removing messages, auth, etc.)

## Requirements
* FastAPI and pymongo are required for this implementation to work
    * ```pip install -r requirements.txt``` to install required libraries
* FastAPI Auth
    * Any access to the database needs to be authenticated
    * [FastAPI Auth Example](https://fastapi.tiangolo.com/advanced/security/http-basic-auth/?h=auth)
* Simple User Interface
    * [Jinja Template HTML](https://www.ibm.com/docs/en/qradar-common?topic=1-jinja2-templates)
* Removing Objects
    * Block messages by user
    * Delete messages (removed flag in data store) by keywords
    * Delete rooms (use a removed flag that can be undone)
    * Delete users (removed flag)
* Sorting Messages
    * Utilize the sequence number (think Binary insert)
* Register/Deregister -> rooms/users
* Metrics for testing

## To Connect with FastAPI
* ```python -m uvicorn *insert API file name*:app --reload```
* The file for the API will be made soon

## Libraries Used
* [Python MongoDB](https://pypi.org/project/pymongo/?msclkid=0eccdbf0ae2311ec8817a467b8e63db2)

## Microservices / API's
* [FastAPI](https://fastapi.tiangolo.com/)
* [MongoDB](https://docs.mongodb.com/manual/?_ga=2.213141972.1346719986.1645739830-1894126807.1645739830)

## Useful Information
* [Basic Message Chat Implementation](https://github.com/kevinthedang/message-based-chat)
* [Message Chat Implementation Mod2](https://github.com/kevinthedang/advanced-message-based-chat)

## Useful Utility
* [Postman](https://www.postman.com/)
* [Python unittest](https://docs.python.org/3/library/unittest.html)
* [Python pytest](https://docs.pytest.org/en/7.1.x/)