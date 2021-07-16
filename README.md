# WARBLER (TWITTER LIKE APP)

This exercise is intended to extend a somewhat-functioning Twitter clone. It is intended to help with giving an understanding of an existing application, as well as fixing bugs in it, writing tests for it, and extending it with new features.

Treating this exercise like a real code base:
- tidy and document as you go
- check into Git often, as you add new features

Practicing this process helps me learn how to work with larger codebases.  

Also, there are a few bugs not mentioned in the app.  Fix these, and keep a log of what you fixed.

## Part One: Fix Current Features
- Understand the Model
- Fix Logout
- Fix User Profile
- Fix User Cards
- Profile Edit
- Research and Understand Login Strategy
    - The logged in user is being kept track of by using the Flask Session Object.  Additionally, it is utilizing Flask’s g object to keep track of current user with Flask Session.  The "add_user_to_g" is called to update the global parameter to match the session user. The "@app.before_request" tells the app to do this function code before a request is even made. 

## Part Two: Add Likes
- Do This Without AJAX/JavaScript
- Add a new feature that allows a user to “like” a warble. They should only be able to like warbles written by other users. They should put a star (or some other similar symbol) next to liked warbles.
- They should be able to unlike a warble, by clicking on that star.
- On a profile page, it should show how many warblers that user has liked, and this should link to a page showing their liked warbles.

## Part Three: Add Tests
- Add tests. You’ll need to proceed carefully here, since testing things like logging in and logging out will need to be tested using the session object.