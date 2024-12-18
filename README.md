# YourDynamicShoppingList
#### Video Demo:  <URL HERE>
#### Description:

In this project, I'm making a web application, where the user can dynamically create a new list and add/delete/modify its item(s). It will also notify the user if any item on the list is on discount, using an API from a government-provided website for grocery discounts in Hungary. Users will also have the possibility to share lists with each other, so everyone can modify the list. 
In the templates folder, you can find all the template pages I used for each route - most of them are only used once per route, and it is always the same. Others, such as shoppinglist.html and homepage.html are dynamically populated: the first is showing the list of items in a given shoppinglist, and the other one is showing a list of shoppinglists for the logged-in user. Layout.html is always present, every other html is an extension of this file. It contains the header part with the navigation buttons, as well as the design elements (SVG for eg.).
In the static folder we can find the images I used, and also some css files for design. In the future, I believe the css files and the images should go to separate folders, but in a same mother-folder, such as 'design'.
Created a separate python file for the backend, called my_flask_app.py. It contains everything that ties together the database, frontend and backend, in coordination with Flask framework.
The database is named YourShopMate.db. It comes from the original name of the project, which was changed later on. In the future, I'd also pay more attention to such details, so everything in the directories are straightforward and aligned.
The database has its own structure too, with 3 tables - items, users, and shoppinglists. The names speak for themselves, but the items table contains data about the items, with a primary key of 'items_id', and a foreign key for 'list_id', that references 'id' from shoppinglists table. Items table has a foreign key of 'creator_id' that references 'users_id' form the users table. The shoppinglists table contains information about the shoppinglists, with a primary key of 'shoppinglists_id', and a foreign key of 'owner_id' and 'coowner_id', that both reference 'users_id' from the users table. The users table contains information about the users, with a primary key of 'users_id'.
There were a lot of structure and design ideas in my mind, how the webapp will look like and function. For example, should the user be able to delete an item, instead of just marking it as completed? Would it be enough, if the items could only be deleted, if the list itself is deleted? I went with adding a separate action icon for this, since there are multiple scenarios, when it can be used, such as if someone makes a mistake, or just wants to keep their list tidy, instead of having many checked items.
Another decision was, if the whole page should refresh, when a list, or item is added, or not - at first, I thought the only way is refreshing the page. But then I realised, that it is not a good design, not a user friendly solution, so I looked for other ways. Found AJAX - only refreshing the part that needs to be updated or modified. Though, later I will come back to this topic, as I believe it could have been set up more efficiently. 
I am using encryption and salting for storing the users passwords - a modern way of storing. Considering to also implement a 'Forgotten password' route, which will not remind the user about their password (since its not stored in the database) but based on verification it sends a link to their email adress, and the link would allow them to change it to a new one.
Using correct alerts for feedback was also an important point - without the correct feedback, it would be hard for the user to navigate. Used the alert styling from Bootstrap, and tried to keep the alert text as short as possible.
Regarding AJAX, it was also hard to set up data transition via API, based on which route is called, and which method is used. Instead of using a shorter syntx, I decided to go with the full-length one, as it was more straightforward for me.
I would also make sure to use row.factory function, as when currently the database connection is opened, and a query runs, it return an array of values, instead of key-value pairs, which would have made the progression better.
In the future, I am planning on implementing 2 features - an API, that notifies users if an (unchecked) item on their list is on discount in a nearby store. It will use information from a governmental site, available for the public.
Another feature would be allowing users to pair their lists, so other users can modify it at the same time. It would be good for households, so everyone can keep adding what they need, avoid duplicates, and check them out together. An updated version of this feature would be allowing not just 2 people to share their lists, but any number of people. Here, we also need to consider verification and security - for example, how can we verify that both parties approve having a list shared.