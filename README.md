# My Book Reviewer
## Video Demo:  https://youtu.be/O9jkTEuWMtw
## Description:
I really like to read books. But after high school I noticed that after a while, I would frequently forget what the books I had read were about. I remember recalling that I had read *The Hound of the Baskervilles* by Arthur Conan Doyle, but I could not remember anything about the book, besides the fact that Sherlock Holmes was there. So I decided that would start writing a small review or summary of each book everytime I finished reading it. I had to reread several books I had read during high school, because my mind had completely erased them from my memory.

So, I started collecting those reviews in a word document, that I have kept updating since that moment. Now, almost 8 or 9 years after, I have been able to collect the reviews of 187 books (I'm not the faster reader, and some books I have read are looooong), and the word document is now 204 pages long. I started with small reviews, but there are some books that I liked so much that I dedicated several pages to them.

I always thought on how to have all these reviews better documented, as now that the word document is so long, searching for a certain review can become a problem, and, even with back ups, I'm always scared of losing it somehow. That's why when I saw that the final project could be an open idea, I did not doubt it for a second that I was going to use it to create an system for my books reviews.

I already work in a job related to computer science and I have worked on projects for web development but with NodeJS, so my main goal for this course was to learn the basics of python, and I was really happy to see that the python learned in the course was focused in web development. So I decided that the solution I was going to create for the final project was going to be using what I had learned on Python and Flask.

## Functionality:
The web app has the following functions:

1. Account registration and log in: The users will have their personal accounts, they will need to register the first time, and log in. The app will save the logged in session.

2. The Books Reviews: The main part of the app. Each user will have their own personal list of reviews. A review consists of the Title of the book, the author's name, a scoring from 0-5 and the personal review. The reviews will be visible from a table in the main page of the app. There are two search inputs, to search by title or by author. From the main view, the user can select to edit a review. The edit button will load a pre-filled form for them to edit the review, or they can delete it all together. The main view also shows the total number of reviews the user has.

3. The Desired Books List: This is an extra feature for those that do not want to forget books they want to read or if they want to share a book for other users to be able to see it and consider it for reading. The app will have a general list of desired books (books that they want to read). From there the user can see books that they themselves or other users have submitted. There are two search inputs, to search by title or by author. From the main table they can see all books (title and author) and add them to their own personal list of desired books. Then they can change the view to just their personal wish list of books they would like to read.

## Files:
### app.py:
This one contains the main functionalities and routing of the application.

#### index:
It gets the whole list of reviews done by the user and the number of reviews done. To send it to the index html page.

#### login:
It does all the necessary validations to confirm that the username and password match. I got the logic from the Problem Set from Week 9.

#### logout:
It clears the session and redirects to the log in page. I got the logic from the Problem Set from Week 9.

#### register:
It does all the necessary validations for the username and password and creates the user in the database, once all security measures were taken. I got the logic from the Problem Set from Week 9, plus my personal touch for the password security measures.

#### review_creator:
It handles POST and GET requests. The GET request, shows the empty form for submitting a new review. And the POST request, handles the creation of the review in the database, after doing the necessary security checks confirming that all information is present.

#### review_editor:
It handles POST and GET requests. The GET request gets the information from the book id provided on the URL, makes sure the book is from the logged in user (to avoid a user editing a book from someone else by changing the number in the URL) and provides this information to the edit-review.html file. If the id is of a book of another user, it just will redirect to the empty form of create-review.

#### review_deleter:
It only handles the GET request. It will delete the review from the id on the URL. But, it does confirm that the book review is from the logged on user. If the id is of a book from another user, it won't do anything and just redirect to the main page.

#### desired_books_index:
It will provide the information of all desired books submitted by users, and also the books from the personal list of the user. This will be used in the file desired-books.html to set the button appropriately depending if the books is or not on the personal list of the user.

#### user_desired_list_index:
It does a join SQL query to provide the information of only the books in the desired list of the user. Same as the general index, it sends the information to desired-books.html

#### desired_books_creator:
It handles POST and GET requests. the GET request, show the empty form for submitting a new book to the desired list (only asking for title and author). The POST request, handles the submission of the book to the list. It confirms that all information is present. It also checks if the book is already on the general list (this is if the title and the author together are already present in the database. If it already exists, it will just get added to the personal list of the user.

#### add_to_list:
It handles the addition of a book from the desired list to the personal list of the logged on user. It confirms that the book id is not missing.

#### remove_from_list:
It handles the removal of a book from the personal list of desired books of the logged on user. It confirms that the book id is not missing.

#### invalid_route:
Error handler for the 404 error. It will show a picture of Patric Star :)

### flask_session:
Contains the session information for the users in the app

### Templates:
The html templates of the app

#### apology.html:
Mostly for handling error messages. It shows a picture of Patric Star with the error.

#### create-desired-book.html:
The form for submitting a new desired book. It asks for the Title and the Author.

#### create-review.html:
The form for submitting a new book review. It asks for the Title, the Author, the points (a numeric input), and the review (a textarea).

#### desired-books.html:
It will show the table with the list of desired books (general or personal). The table contains three columns: The title, the author and the button to either add or remove from the book from the personal list. Two search boxes to search by title and author (managed through some JS code, taken from W3Schools). A button will show at the top to change the view from general to personal list or viceversa. Also a button that will take you to the submit form.

#### edit-review.html:
The same form for submitting a book review. But this one contains the logic for prefilling the form with the information of the book that will be editted. Also a button to delete the review.

#### index.html:
It will show the table with the list of reviews done by the user. the table contains four columns: The title, the author, the puntuation (with a for range loop dependant of the points given) and the review. The review contains a link to edit the review. Two search boxes to search by title and author (managed through some JS code, taken from W3Schools). The top of the table will contain the number of reviews saved.

#### layout.html:
General layout of the application. Mostly taken from the Problem Set from Week 9. It provides the nav bar that takes the user to My Reviews, Create Review or the Desired Books. Also the options to Log out or Log in and Register, depending if the user is already logged in or not. It also contains the links for Bootstrap and the css stylesheet. And a footer at the bottom of the page.

#### login.html:
Mostly taken from the Problem Set of Week 9, it shows the login form.

#### register.html:
Mostly taken from the Problem Set of Week 9, it shows the registry form.

### static:
Contains the icon and the css styles sheet

#### favicon.ico:
The books icon for the browser tab.

#### script.js:
Contains the script taken from W3Schools for searching on the tables. It does the searching directly on the browser, so it does not check back the database. Two functions (one for the title and one for the author).

#### styles.css:
Contains the css styling of the website.

### books.db:
The database for the application:

#### users:
Contains the user information: id, username and password hash. An index was created for the usernames.

#### book_reviews:
Contains the information of the book reviews: id, user_id (user that did the review), title, author, review and points. An index was created for the book titles.

#### desired_books:
Contains the inforamtion of the desired books: id, title and author.

#### desired_books_users:
Links the tables users and desired_books linking the user_id and the desired_book_id. This is because it is a many to many relation (a user can have several desired books, and a book can be in the desired list of several users). An index was created for the book titles.