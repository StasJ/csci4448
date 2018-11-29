from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.template import loader, Context


## \mainpage
#
# Welcome to the Forum documentation
#
# \par
#
# <a href="classes.html">Link to the class index</a>
#


## @class Topic
#
# @brief Topic under which a post can be categorized
#
class Topic(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    ## 
    # @return Primary Key
    #
    def getId(self):
        return self.id

    ## 
    # @return Name of topic
    #
    def getName(self):
        return self.name

    ## 
    # @param[in] name Name of topic
    #
    def setName(self, name):
        self.name = name


## @class Post
#
# Post class represents a post.
# It keeps track of a post as well as providing utility functions
#
class Post(models.Model):
    user   = models.ForeignKey(User,  on_delete=models.CASCADE)
    topic  = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    title  = models.CharField(max_length=256, blank=True)
    text   = models.TextField()
    date   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if (self.parent):
            return "Reply to " + self.parent.title
        return self.title

    def getId(self):
        return self.id

    def getUser(self):
        return self.user

    def setUser(self, user):
        self.user = user
    
    def getTopic(self):
        return self.topic

    def setTopic(self, topic):
        self.title = topic

    def getTitle(self):
        return self.title

    def setTitle(self, title):
        self.title = title

    def getText(self):
        return self.text

    def setText(self, text):
        self.text = text

    def getVotes(self):
        return self.vote_set.all()

    def getNumberOfVotes(self):
        return self.vote_set.count()

    ##
    # This function toggles a user's vote. If a user has not yet voted on a post
    # this will create a new vote for them. If they have, this will remove their
    # vote
    #
    # @param[in] user that is voting
    #
    # @return Vote on create vote
    # @return None on delete vote
    #
    def toggleVote(self, user):
        vote, created = Vote.objects.get_or_create(user=user, post=self)
        if created:
            vote.save()
            return vote
        else:
            vote.delete()
            return None



## @class Vote
#
# @brief Vote class represents a vote. It keeps track of a unique user and post pair
#
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.post.title + " : " + self.user.username

    ## 
    # @return User that voted
    #
    def getUser(self):
        return self.user

    ## 
    # @param[in] user User that voted
    #
    def setUser(self, user):
        self.user = user
    
    ## 
    # @return Post to vote on
    #
    def getPost(self):
        return self.post

    ## 
    # @param[in] post Post to vote on
    #
    def setPost(self, post):
        self.post = post
    

    class Meta:
        unique_together = ('user', 'post')



## @class UserMeta
#
# @brief Holds additional user data
#
class UserMeta(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    key   = models.CharField(max_length=256)
    value = models.TextField(blank=True)

    def __str__(self):
        return self.user + ": " + self.key + " = " + Truncator(self.value).chars(50)

    ## 
    # @return User associated with metadata
    #
    def getUser(self):
        return self.user

    ## 
    # @param[in] user Set user
    #
    def setUser(self, user):
        self.user = user

    ## 
    # @return string key
    #
    def getKey(self):
        return self.key

    ## 
    # @param[in] key Set key
    #
    def setKey(self, key):
        self.key = key

    ## 
    # @return string value for key
    #
    def getValue(self):
        return self.value

    ## 
    # @param[in] value
    #
    def setValue(self, value):
        self.value = value


## @class BaseUser
#
# @brief Superclass for User objects
#
class BaseUser():
    def __init__(self, user):
        self.user = user

    def __str__(self):
        return str(self.user)

    def getId(self):
        return self.user.id

    def getFullName(self):
        return self.user.get_full_name()

    def getEmail(self):
        return self.user.email

    def getDateJoined(self):
        return self.user.date_joined

    def getLastLogin(self):
        return self.user.last_login

    def getPostCount(self):
        return self.user.post_set.count()

    def getPersonalPageTemplate(self):
        return loader.get_template('forum/personal_page.html')

    ## 
    #
    # If a user has a personal page, this function renders a section containting
    # the personal page.
    #
    # If this function is called on an Admin user, it returns a personal page that
    # simply states it is an admin account.
    #
    # @return string of rendered template
    #
    def getPersonalPage(self):
        return ""

    ## 
    # Only sets the personal page for a member
    #
    def setPersonalPage(self, text):
        pass

    ##
    # @return list<Post>
    #
    def getPosts(self):
        return self.user.post_set.all()


## @class Admin
#
# @brief Representation of an admin user
#
class Admin(BaseUser):
    def __init__(self, user):
        super().__init__(user)

    ## 
    #
    # Creates a new topic
    #
    # @return Topic newly created topic. This topic is not yet saved.
    #
    def createTopic(self, name):
        topic, created = Topic.objects.get_or_create(name=name)
        return topic


    ## 
    #
    # Returns a personal page that simply states it is an admin account.
    #
    # @return string of rendered template
    #
    def getPersonalPage(self):
        template = self.getPersonalPageTemplate()
        return template.render({'page': "This is an administrator account."})


## @class Member
#
# @brief Representation of a typical member of the site
#
class Member(BaseUser):
    def __init__(self, user):
        super().__init__(user)
        pageMeta, created = UserMeta.objects.get_or_create(user=user, key='page')
        if not created:
            self.page = pageMeta.value
        else:
            self.page = None

    ## 
    #
    # If a user has a personal page, this function renders a section containting
    # the personal page.
    #
    # @return string of rendered template
    #
    def getPersonalPage(self):
        template = self.getPersonalPageTemplate()
        return template.render({'page': self.page})

    def setPersonalPage(self, text):
        pageMeta, created = UserMeta.objects.get_or_create(user=self.user, key='page')
        pageMeta.value = text
        pageMeta.save()



## @class FactoryBase
#
# @brief Base Factory class for the Factory design pattern
#
class FactoryBase():
    def create(self, value):
        pass


## @class UserFactory
#
# @brief Creates Admin or Member classes to represent the User model passed in
#
class UserFactory(FactoryBase):
    
    ##
    # @return BaseUser
    #
    def create(self, userModel):
        if userModel.is_staff:
            return Admin(userModel)
        else:
            return Member(userModel)


