*******--MUST Read the Document--***********

1) At first Unzip the file and install all the dependencies recorded in <requirements.txt> file. This file is Updated No Need to change anything.

2) After installing the dependencies just run the project with this command <python manage.py runserver> (Make sure you are in the correct directory).

3) There are 2 Views declared in the app. 1st one is API_View (This is what we need for Airbnb). And 2nd one is Web View. I Created the web View for testing and debugging purpose. You Don't need to manipulate any code here.


**IMPORTANT**

4) Now just POST a JSON Request to the API End-point <localhost/api/sentiment/> The JSON Format is given Below:
{
    "sentence":"Your Review Here."
}

Here, the Key will be "sentence" and the value will be "Your Review Here". You have to use the POST method. Upon requesting, You will receive a response like this :
{
    "sentence": "Your Review Here",
    "sentiment": "Neutral"
}


NB: Please make sure that you change the DATABASE Connection String. Currently it is using my MongoDB Cloud DATABASE.

That's It. 
Gd Luck.