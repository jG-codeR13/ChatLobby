# chit-chat-room
A real-time chat room application in Flask using socketio.

* __Multiple Rooms__: Using `Flask-Socketio` different rooms are created for different types of discussions.
* __Profanity Filtering__: Using `better-profanity` python module all swear words (and their leetspeak) are removed from message strings.
* __Live Chat__:  all messages are sent to the Python web server, and then broadcast back to all clients.
* __Register/Login__: Using `flask-sqlalchemy` all users are registered and can login again with same username-password.

![demo](https://github.com/bhu800/chit-chat-room/blob/master/Screenshots_gifs/demo5.gif)

## How to deploy ?


 
 Access the web app in browser: http://127.0.0.1:5000

## What's next ?
- [x] Build a basic chat application with pre-existing different rooms.
- [x] **Bad word filtering**
- [ ] Custom Bad word filtering and warning and user removing feature on consistent use of bad words
- [ ] 'Add Room' functionality 
- [ ] show all online users
- [ ] emojis and stickers for chat
- [ ] Joining multiple rooms at a time
- [ ] Add, Update and View Profile (Profile Image, About) (basicaly a little 'social' touch :D)
- [ ] Different background-image for different lounge
- [ ] Admin Backend, so that some sort of events and discussions can be hosted on the platform
- [ ] Join as guest (no register/login required) feature.
- [ ] Join via __`invite-link`__ feature (room creater can send invite link for __private rooms__)
- [ ] Permission feature if room creator wants to let specific persons to let in. There can be multiple methods to verify/permit user: a.) Email verification b.) Allowing only educational email ids with verification c.) manual perimitting by room-admin.
- [ ] Share admin power feature in which admin can make further new admins or moderators fo same room.
