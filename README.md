# Nails Beauty
## This is an individual project assignment for the course "Python Web Framework" at SoftUni
### Table of Contents

* [1. Introduction](#chapter1)
* [2. Website Overview](#chapter2)
    * [2.1. Users and Profiles](#section_2_1)
        * [2.1.1. Anonymous User](#section_2_1_1)
        * [2.1.2. Registered User](#section_2_1_2)
        * [2.1.3. Administrative User](#section_2_1_3)
        * [2.1.4. Profile Characteristics](#section_2_1_4)
    * [2.2. Feedback](#section_2_2)
        * [2.2.1. Feedback Characteristics](#section_2_2_1)
        * [2.2.2. Feedback Likes](#section_2_2_2)
* [3. Tests Coverage](#chapter3)
* [4. Additional Developments](#chapter4)

### 1. Introduction <a class="anchor" id="chapter1"></a>

Website users have the opportunity to create their own accounts and publish their feedback. Each feedback can be liked by other users. Each user collects their own feedback and likes from other
users.

### 2. Website Overview <a class="anchor" id="chapter2"></a>

Both registered and unregistered users have access to the website.

Unregistered users have the opportunity to view only the feedback of registered users, and they cannot like them.

Registered users have the opportunity to create their own profiles and leave feedback. They may not like the feedback they have.

In the following described in detail the functionality of the objects.

#### 2.1. Users and Profiles <a class="anchor" id="section_2_1"></a>

A ***Custom User Model*** has been implemented to create a user objects so that the email address can be used as the
primary user ID instead of the authentication username.

The user objects have relational connections to all other objects in the project.

In terms of registration, users are:

- Anonymous User
- Registered users
- Administrative users

The accounts (profiles) objects have a relational connection "OnetoOne" with pre-created users.

##### 2.1.1 Anonymous User <a class="anchor" id="section_2_1_1"></a>

The ***anonymous user*** has permission to view only all public post and their details. This user has restricted access
to the navigation bar. He is able to register in the website with an email and password. The registration includes an
email verification process. Once this user has registered and logged in to the website he has access to the rest of the
functionality.

##### 2.1.2 Registered User <a class="anchor" id="section_2_1_2"></a>

The ***registered user*** is already registered and can log in with an email and password. After his authentication, the
user is able to navigate through the navigation bar. The registered user has his own profile with image,
first name, last name, phone number, age. This user has all CRUD permissions to his own feedback. He can like
all feedback in the system, except his own.

##### 2.1.3 Administrative User <a class="anchor" id="section_2_1_3"></a>

The ***administrative user*** gets enabled through the admin site by the superuser. His 'is_staff' field is set to True.
This user has all CRUD permissions over other users and their posts in the database.

##### 2.1.4 Profile Characteristics <a class="anchor" id="section_2_1_4"></a>

Every registered user has an account ***(profile)***. The profile allows the user to change his password, to update his
own information and to delete his own account. The profile page shows the completion of the user's profile and his
feedback. The ***profile*** can be completed up to 100% after all fields in the form are filled out. Each registered user can see other user profiles and their feedback.

The ***profile*** has the following fields:

- first name - CharField with max length 20 chars
- last name - CharField with max length 20 chars
- phone number - CharField max length 17 chars and validator for phone number
- age - IntegerField
- profile image - ImageField

#### 2.2. Nails <a class="anchor" id="section_2_2"></a>

The ***nails*** could be either public or private. It can be viewed by all types of users but created, edited, and
deleted only by its author. The author can't like his own ***nails***. Only the other users
can like it.

##### 2.2.1 Nails Characteristics <a class="anchor" id="section_2_2_1"></a>

The ***nails*** has the following fields:

- type - CharField with max length 10 chars and choices options
- feedback - CharField with max length 10 chars and choices options
- description - CharField with max length 200 chars
- user - ForeignKey relation with nails user


##### 2.2.2 Nails Likes <a class="anchor" id="section_2_2_2"></a>

The ***nails likes*** are public. It can be viewed by all types of users. The author and
anonymous users can't like the ***nails***. Only the other users can like it. Once the like object is created by a
single user, can be  deleted on clicked again.

The ***nails likes*** has the following fields:

- nails - ForeignKey relation with nails
- user - ForeignKey relation with nails user


### 3. Tests Coverage <a class="anchor" id="chapter3"></a>


### 4. Additional Developments <a class="anchor" id="chapter4"></a>

- :heavy_check_mark: Responsive web design
- :heavy_check_mark: Class-based views
- :heavy_check_mark: Extended Django user
- :x: Documentation/ Swagger
- :heavy_check_mark: Use a file storage cloud API e.g., Cloudinary, Dropbox, Google Drive or other for storing the files
- :x: Implement Microservice architecture in your application.
- :heavy_check_mark: Additional functionality, not explicitly described in this section, will be counted as a bonus if it has practical
  usage.
