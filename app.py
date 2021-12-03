from db import db
from flask import Flask, request
from db import User, Post, Purchase, Review
import json
import os

app = Flask(__name__)
db_filename = "eBay.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.drop_all()
    db.create_all()
    new_user = User(name="overlord", username="fake", balance= 100, password= "hi")
    db.session.add(new_user)
    db.session.commit()
    for name, desc in [("CS 1110", "Introduction to Computing using Python"),
    ("CS 2110", "Object-Oriented Programming and Data Structures"),
    ("CS 2800", "Discrete Structures"), 
    ("CS 3110", "Data Structures and Functional Programming"), 
    ("CS 3410", "Computer System Organization and Programming"), 
    ("CS 4410", "Operating Systems"), 
    ("CS 4820", "Introduction to Analysis of Algorithms")]:
        new_class= Post(
            title= name,
            description= desc, 
            price= 5,
            is_completed= False
        )
        db.session.add(new_class)
        seller= User.query.filter_by(id= 1).first()
        seller.posts.append(new_class)
        db.session.commit()

def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(message, code=404):
    return json.dumps({"error": message}), code

"""
Routes
"""
@app.route("/api/users/", methods=["GET"])
def get_users():
    return success_response(
        {"users": [s.serialize() for s in User.query.all()]}
    )

@app.route("/api/users/<int:user_id>/")
def get_user(user_id):
    user = User.query.filter_by(id = user_id).first()
    if user is None:
        return failure_response("User does not exist!")
    return success_response(user.serialize())

@app.route("/api/users/", methods=["POST"])
def create_user():
    body = json.loads(request.data)
    missing_items= []
    if body.get("name") == None:
        missing_items.append("name, ")
    if body.get("username") == None:
        missing_items.append("username, ")
    if body.get("password") == None:
        missing_items.append("password, ")
    if missing_items != []:
        res= "Must include "
        for item in missing_items:
            res += item
        return failure_response(res.strip(", ") + "!", 400)
    new_user = User(name=body.get("name"), username=body.get("username"), balance= body.get("balance", 0), password= body.get("password"))
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)

@app.route("/api/users/<int:id>/", methods=["DELETE"])
def delete_user(id):
    user= User.query.filter_by(id=id).first()
    if user is None:
        return failure_response("User not found!")
    db.session.delete(user)
    db.session.commit()
    return success_response(user.serialize())

@app.route("/api/courses/<int:id>/", methods= ["POST"])
def create_post(id):
    body= json.loads(request.data)
    if body.get("description") == None:
        if body.get("price") == None:
            return failure_response("A description and price must be provided!", 400)
        return failure_response("A descripion must be provided!", 400)
    if body.get("price") == None:
        return failure_response("A price must be provided!", 400)
    new_post= Post(
        title= body.get("title"),
        description= body.get("description"), 
        price= body.get("price"),
        is_completed= False
    )
    db.session.add(new_post)
    seller= User.query.filter_by(id= id).first()
    if seller is None:
        return failure_response("User not found!")
    seller.posts.append(new_post)
    response= new_post.serialize()
    response["seller_id"]= id
    db.session.commit()
    return success_response(response, 201)

@app.route("/api/courses/", methods=["GET"])
def get_posts():
    return success_response(
        {"courses": [p.serialize() for p in Post.query.all()]}
    )

@app.route("/api/courses/<int:post_id>/")
def get_post(post_id):
    post = Post.query.filter_by(id = post_id).first()
    if post is None:
        return failure_response("Course does not exist!")
    return success_response(post.sub_serialize())

@app.route("/api/courses/<int:id>/transactions/", methods=["POST"])
def execute_transaction(id):
    body= json.loads(request.data)
    post= Post.query.filter_by(id=id).first()
    if post is None:
        return failure_response("Post not found!")
    if post.is_completed:
        return failure_response("This item is no longer for sale", 400)
    buyer= User.query.filter_by(id=body.get("buyer_id")).first()
    seller= post.seller[0]
    if post.price > buyer.balance:
        return failure_response("You have insufficient funds!", 400)
    buyer.balance -= post.price
    seller.balance += post.price
    new_purchase= Purchase(
        price= post.price
    )
    db.session.add(new_purchase)
    buyer.purchases.append(new_purchase)
    seller.sales.append(new_purchase)
    post.is_completed= True
    db.session.commit()
    return success_response(post.serialize(), 200)

"""
id is for the post
"""
@app.route("/api/courses/<int:id>/reviews/", methods=["POST"])
def create_review(id):
    body= json.loads(request.data)
    reviewed_item= Post.query.filter_by(id=id).first()
    #if reviewed_item.is_completed != True:
    #    return failure_response("This item hasn't been purchased!", 400)
    #if reviewed_item.review != []:
    #    return failure_response("This item has already been reviewed!", 400)
    if reviewed_item == None:
        return failure_response("Course does not exist!")
    new_review= Review(
        rating= body.get("rating"),
        review= body.get("review")
    )
    valid_ratings= [1,2,3,4,5]
    if new_review.rating not in valid_ratings:
        return failure_response("Rating must be an integer 1 through 5!", 400)
    reviewed_item.review.append(new_review)
    #seller= reviewed_item.seller[0]
    #seller.items_reviewed += 1
    #seller.total_rating += body.get("rating")
    #seller.seller_rating = seller.total_rating / seller.items_reviewed
    db.session.commit()
    return success_response(new_review.serialize(), 201)

@app.route("/api/courses/<int:id>/reviews/", methods=["DELETE"])
def delete_review(id):
    reviewed_item= Post.query.filter_by(id=id).first()
    review= reviewed_item.review[0]
    if review is None:
        return failure_response("Review not found!")
    seller= reviewed_item.seller[0]
    seller.items_reviewed -= 1
    seller.total_rating -= review.rating
    if seller.items_reviewed != 0:
        seller.seller_rating = seller.total_rating / seller.items_reviewed
    elif seller.items_reviewed == 0:
        seller.seller_rating = 0
    db.session.delete(review)
    db.session.commit()
    return success_response(review.serialize())

    


    

    


if __name__ == "__main__":
    port = os.environ.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)