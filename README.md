# hackChallenge
Backend Description:
We originally designed our backend as an online marketplace platform that allowed users to create accounts, post items to sell, and review those items afterwards, but ended up changing our app to a course review platform, so parts of our backend weren't used. Quick note: an object of type Post is meant to represent a single course. First we provide a description of our routes and models that ended up being used:
- GET /api/courses/ : this returns all of the courses that have already been added to the database, including that course's id number and title
- GET /api/courses/<int:post_id>/ : this finds and returns a serialized version of a course with id <int:post_id>, including that course's id, title, description, and a list of reviews
- POST /api/courses/<int:id>/reviews/ : this requests a rating (an int in 1..5) and an optional review (String description of review), and creates a new review that is added to the list of reviews for the course with the id <int:id>
- association_table2 allows for a relationship between one post and many instances of reviews
- since posts have a seller and thus require a relationship to a user, we create a fake user to connect to each post

Routes/Relationships not used:
- GET /api/users/ : returns a list of all users
- POST /api/users/ : requests a name, username, an optional balance, and a password, and creates a user with these inputs
- GET /api/users/<int:user_id>/ : returns a user with id <int:user_id>
- DELETE /api/users/<int:id>/ : deletes a user with id <int:id>
- POST /api/courses/<int:id>/ : requests a title, description, and price and creates a new Post
- POST /api/courses/<int:id>/transactions/ : requests the id of a buyer and executes a transaction by fulfilling the purchase of the post with id <int:id>; updates balances of buyer and seller; checks if buyer has appropriate balance; creates a new Purchase to add to buyer's purchase history, as well as seller's sale history
- DELETE /api/courses/<int:id>/reviews/ : if an item is purchased and reviewed, it deletes that item's review
- association_table allows for a relationship between a user and their posts
- association_table3 allows for a relationship between a Purchase and the buyer in the Purchase/transaction
- association_table4 allows for a relationship between a Purchase and the seller in the Purchase/transaction


1. Big Red Course Reviews
2. Lists CS courses at Cornell where users can read and leave their own reviews of the course
3. ios
4. add screenshots
5. Users can browse through classes, and click on one to see more information. There they can read reviews and leave one of their own.
6. ios idk, backend - http://bigredcoursereviews.herokuapp.com/ /api/courses/ to see all courses, /api/courses/id/ to see a specific course, /api/courses/id/reviews/ to leave a review. We have other routes that we did not end up using on the frontend and our backend has 3 tables that have relationships (classes, reviews, users(not used)).
7. We initially were making a marketplace app, which is why we have users and transaction routes. We later dicided to make a course reviews app and wanted to modify what we already had instead of starting over.
