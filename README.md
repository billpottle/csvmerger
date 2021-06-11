# csvmerger
A general python GUI file to intelligently merge any 2 CSV files. 

This file was written for a non-profit to be able to merge data from different systems (volunteers, donors, vendors, event attendees, social media fans, etc) to one file while identifying and merging data from records that are likely to be from the same person. 

![screenshot of csv merger](https://github.com/billpottle/csvmerger/blob/main/screenshot.jpg?raw=true)

**Features:** 

* Can handle any number of matching conditions in the format (A AND B) or (C) or (D AND E). For instance, "First Name" equals 'fname' AND "Last Name" equals 'lname' OR 'email' = 'primary contact email' 

* Can merge certain columns whether or not they match. 

* Can handle custom equality conditions (ie, eventId(42) = eventName('Winter Banquet') through the nickname function. 

* Allows user to select case sensitivity. 

**Instructions:**

1) Windows users can download the files in the dist folder and then click on main.py to run

or 

2) Alternatively, clone the repo to run from source. This Requires python to be installed on your local system. Run the file with 'python main.py'



Uses nickname list and code from
https://github.com/carltonnorthern/nickname-and-diminutive-names-lookup
