<!-- Title -->

<!-- Headers and sub headers -->

<!-- Introduction [intro, techstack] -->

# Django Chat Server

## Introduction

Django Chat Server is a chat application built on top of the Django framework. It provides a real-time communication platform for users, enabling them to engage in seamless conversations, share multimedia content, and collaborate effectively.

### Tech stack
- Django
- Django_rest_framework
- Django channels
- Redis
- Swagger (for docs)

### Features

- **Real-time Messaging:** Enjoy instant messaging with real-time updates.
- **User Authentication:** Secure user authentication and authorization.
- **Multimedia Support:** Share images and files in your conversations.


## How it Works
The Django chat server facilitates user communication within accessible rooms by enabling the transmission of messages. Additionally, users can establish WebSocket connections to seamlessly receive real-time messages through the implementation of Django Channels. Upon establishing a WebSocket connection, a new Django Channels instance is dynamically generated, fostering bidirectional interaction with the user. 

This channel instance is configured to subscribe to the user's associated rooms, allowing it to monitor incoming messages in real-time. In the event that **a user joins a new group**, the server promptly adds the group to the existing channel, ensuring instantaneous reception of real-time messages from the newly joined group.

Furthermore, upon termination of a WebSocket connection, the server initiates the unsubscription of the channel instance from the associated groups. This proactive measure is undertaken to optimize resource utilization and maintain system efficiency.

- The system also supports the establishment of a global limit for users within groups or rooms. This functionality can be configured by accessing the `MAX_USERS_IN_ROOM` option within the designated directory path: config/settings.


## Quick Start

- Make sure to create a `.env` file in the root directory and copy the contents of `.env-example` in it, Then replace the environment variables with your own.
- You can use either of **installation with docker** or **virtual environment** methods, I suggest you go with the docker setup since it makes the process smooth and easy as possible.

## Installation via docker

1. Clone the repository:

   ```bash
   git clone https://github.com/jordanos/django-chat-server.git
   cd django-chat-server
   ```

2. Run `docker-compose build` then `docker-compose up`. This will build and start the app on port 8000.

## Installation via virtual environment on local machine

Dependencies
- PostgreSQL - You must have postgresql running on your machine. 
- Redis - You must have redis running on your machine.

1. Clone the repository:

   ```bash
   git clone https://github.com/jordanos/django-chat-server.git
   cd django-chat-server
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

6. Run the development server:

   ```bash
   python manage.py runserver
   ```

The Django Chat Server will be accessible at `http://localhost:8000/`.


## API Schema

The Django Chat Server exposes a RESTful API for seamless integration with other applications. **The schema is documented with swagger** and you can access it at `http://localhost:8000/api/v1/` or read the docs at `http://localhost:8000/api/v1/redoc/`. Below is an overview of the API endpoints:

### Authentication

- **POST /api/token/**

  Request Token for Authentication.

  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```

  Response:

  ```json
  {
    "token": "your_token",
  }
  ```



- Except the `Users` endpoint every other one **requires an authenticated user**. so, providing the authentication token in the authorization header is necessary. Authorization: `Token <your_token>`.


### User Endpoints

- **GET /api/v1/users/**

  Get a list of users.

- **POST /api/v1/chats/user/**

  Create a user

- **PATCH /api/v1/chats/user/{user_id}/**

  update a user

- **DELETE /api/v1/chats/user/{user_id}/**

  delete a user


### Room Endpoints

- **GET /api/v1/chats/rooms/**

  Get a list of all available chat rooms the user has joined.

- **POST /api/v1/chats/rooms/**

  Create a chat room

- **PATCH /api/v1/chats/rooms/{room_id}/**

  Update a chat room

- **DELETE /api/v1/chats/rooms/{room_id}/**

  Delete a chat room

- **PUT /api/v1/chats/rooms/{room_id}/join/**

  Join a chat room

- **PUT /api/v1/chats/rooms/{room_id}/leave/**

  Leave a chat room

### Messaging Endpoints

- **GET /api/v1/chats/messages/**

  Get a list of messages the current user has access to.

- **GET /api/v1/chats/messages/?room={room_id}**

  Get a list of messages filtered by room.

- **POST /api/v1/chats/messages/**

  Create a message.

- **UPDATE /api/v1/chats/messages/{message_id}/**

  Update a message.

- **DELETE /api/v1/chats/messages/{message_id}/**

  Delete a message.


## Websocket

Listening on `wss://localhost:8000/` will do the trick. however, since every websocket connection requires an authenticated user, please provide your token like this `wss://localhost:8000/?token={your_token}`. This websocket receives all incoming messages from the rooms the user has joined to.

- **Send message with websocket**

  ```json
  {
    "text": "your_message",
    "room": "room_id"
  }
  ```

- If attaching files is required, You have to use the rest API endpoint to create a message and send it as multipart form data. Using django signals, this has been made to operate in real-time and every other websocket connection including the current user gets the new message instantly.