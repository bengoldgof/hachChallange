from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

"""
Association Table(s)
"""

association_table= db.Table(
    "association",
    db.Model.metadata,
    db.Column("user_id", db.ForeignKey("user.id")),
    db.Column("post_id", db.ForeignKey("post.id"))
)

association_table2= db.Table(
    "association2",
    db.Model.metadata,
    db.Column("post_id", db.ForeignKey("post.id")),
    db.Column("review_id", db.ForeignKey("review.id"))
)

association_table3= db.Table(
    "association3",
    db.Model.metadata,
    db.Column("user_id", db.ForeignKey("user.id")),
    db.Column("purchase_id", db.ForeignKey("purchase.id"))
)

association_table4= db.Table(
    "association4",
    db.Model.metadata,
    db.Column("user_id", db.ForeignKey("user.id")),
    db.Column("purchase_id", db.ForeignKey("purchase.id"))
)


"""
Classes
"""

class User(db.Model):
    __tablename__= "user"
    id= db.Column(db.Integer, primary_key= True)
    name= db.Column(db.String, nullable= False)
    username= db.Column(db.String, nullable= False)
    password= db.Column(db.String, nullable= False)
    balance= db.Column(db.Integer)
    posts= db.relationship("Post", secondary= association_table, back_populates= "seller")

    purchases= db.relationship("Purchase", secondary= association_table3, back_populates= "buyer")

    sales= db.relationship("Purchase", secondary= association_table4, back_populates= "seller")
    items_reviewed= db.Column(db.Integer, nullable= False)
    total_rating= db.Column(db.Integer, nullable= False)
    seller_rating= db.Column(db.Integer, nullable= False)
    

    def __init__(self, **kwargs):
        self.name= kwargs.get("name")
        self.username= kwargs.get("username")
        self.balance= kwargs.get("balance")
        self.password= kwargs.get("password")
        self.items_reviewed, self.total_rating, self.seller_rating = 0, 0, 0
        

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "balance": self.balance,
            "posts": [p.sub_serialize() for p in self.posts],
            "purchases": [p.sub_serialize() for p in self.purchases],
            "sales": [p.sub_serialize() for p in self.sales],
            "rating": self.seller_rating
        }
    
    def sub_serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username
        }

class Purchase(db.Model):
    __tablename__= "purchase"
    id= db.Column(db.Integer, primary_key= True)
    buyer= db.relationship("User", secondary= association_table3, back_populates= "purchases")
    seller= db.relationship("User", secondary= association_table4, back_populates= "sales")
    price= db.Column(db.Integer, nullable= False)

    def __init__(self, **kwargs):
        self.price= kwargs.get("price")

    def serialize(self):
        return {
            "id": self.id,
            "buyer": [p.sub_serialize() for p in self.buyer],
            "seller": [p.sub_serialize() for p in self.seller],
            "price": self.price
        }


    def sub_serialize(self):
        return {
            "id": self.id,
            "price": self.price
        }

class Post(db.Model):
    __tablename__= "post"
    id= db.Column(db.Integer, primary_key= True)
    seller= db.relationship("User", secondary= association_table, back_populates= "posts")
    title= db.Column(db.String, nullable= False)
    description= db.Column(db.String, nullable= False)
    price= db.Column(db.Integer, nullable= True)

    is_completed= db.Column(db.Boolean, nullable= True)
    review= db.relationship("Review", secondary= association_table2, back_populates= "item")

    def __init__(self, **kwargs):
        self.title= kwargs.get("title")
        self.description= kwargs.get("description")
        self.price= kwargs.get("price")
        self.is_completed= kwargs.get("is_completed")

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
        }

    def sub_serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "reviews": [p.sub_serialize() for p in self.review]
        }

class Review(db.Model):
    __tablename__= "review"
    id= db.Column(db.Integer, primary_key= True)
    rating= db.Column(db.Integer, nullable= False)
    review= db.Column(db.String)
    item= db.relationship("Post", secondary= association_table2, back_populates= "review")

    def __init__(self, **kwargs):
        self.rating= kwargs.get("rating")
        self.review= kwargs.get("review")

    def serialize(self):
        return {
            "id": self.id,
            "rating": self.rating,
            "review": self.review,
            "reviewed_course": [p.serialize() for p in self.item]
        }
        
    def sub_serialize(self):
        return {
            "rating": self.rating,
            "review": self.review
        }