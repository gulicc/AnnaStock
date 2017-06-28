# -*- coding: utf-8 -*-
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
import datetime

connect("mongodb://localhost:27017/dbtest")

class User(MongoModel):
    email = fields.EmailField(primary_key=True)
    first_name = fields.CharField()
    last_name = fields.CharField()

class Comment(EmbeddedMongoModel):
    author = fields.ReferenceField(User)
    content = fields.CharField()

class Post(MongoModel):
    title = fields.CharField()
    author = fields.ReferenceField(User)
    revised_on = fields.DateTimeField()
    content = fields.CharField()
    comments = fields.EmbeddedDocumentListField(Comment, default=[])

uu = User('user@email.com', last_name='Ross', first_name='Bob').save()

post = Post(author=uu, title='PostTitle', content='This is the first post!').save()

comment = Comment(uu, 'Another comment')
post.revised_on = datetime.datetime.now()

post.comments.append(comment)

post.save()

for user in User.objects.all():
    print(user.first_name + ' ' + user.last_name)

month_ago = datetime.datetime.now() - datetime.timedelta(days=30)
for post in Post.objects.raw({'revised_on': {'$gte': month_ago}}):
    print(post.title + ' by ' + post.author.first_name)