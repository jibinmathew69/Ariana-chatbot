# README #

This repository is a Django test task project for Ariana Health, which contains a chat agent. 

### What is this repository for? ###
Django Rest APIs for chatbot.

### How do I get set up? ###

Run the following step to get up and running with the project:

#### Dependency
The application runs on Python3.6<br>
Run following code in commandline at the root of folder:

`pip install -r requirements.txt`

#### Database

Run following code in commandline at the root of folder:

`python manage.py migrate`

#### Run application 
`python manage.py runserver`

The application opens up at 127.0.0.1:8000

#### Run Tests
`python manage.py test`



## API list

base url = 127.0.0.1

* /questionaire/ - GET/POST/PUT/DELETE for Questionaires - Use for listing questionaires
* /questions/ - GET/POST/PUT/DELETE for Questions
* /responses/ - GET/POST/PUT/DELETE for Response options for Questions in Questionaires
* /chat/chat/ - GET/POST/PUT/DELETE for Chat history of User
* /chat/chattree - POST for uploading json file of dialog tree<br>
Parameters : <br>
name : Questionaire Name [Text]<br>
file : Questionaire Json File [File]

* /chat/chatbot - POST for uploading json file of dialog tree
Parameters : <br>
questionaire : Questionaire id [Integer] (Obtained from GET /questionaire/ api)<br> 
message : User's Input [Text]

#### Using Chatbot API

* Chat is initiated by sending an POST API request to /chat/chatbot, which return a Question
along with possible option.<br>
Sample reponse:<br>
```json
{
    "question": "What would you like to eat?",
    "response": [
        "Hamburger",
        "Pizza",
        "Pop Corn",
        "Chicken"
    ]
}
```

* When the chat tree is executed as per User input and chat tree, keep using POST API request to /chat/chatbot
* When chat is exhausted, and there is no options for the response from user POST API request to /chat/chatbot returns 
`Restarting Conversation:` along with chat history.<br>
Sample reponse:<br>
`"Restarting Conversation: Are you hungry?->yes->Pizza->yes"`


#### JSON file structure
```json
[
  {
    "id" : 1,
    "question" : "Are you hungry?",
    "response" : {
      "Yes" : 2,
      "No" : 3
    }
  },
  {
    "id" : 2,
    "question" : "What would you like to eat?",
    "response" : {
      "Hamburger": 4,
      "Pizza": 5,
      "Pop Corn": 6,
      "Chicken": 7
    }
  },
  {
    "id": 3,
    "question": "Ok. Call me when you're hungry.",
    "response": {}
  },
  {
    "id" : 4,
    "question" : "Nice, I will order a hamburger for you!",
    "response" : {}
  },
  {
    "id" : 5,
    "question" : "Would you like pizza with mushrooms?",
    "response" : {
      "Yes": 8,
      "No": 9
    }
  },
  {
    "id" : 6,
    "question" : "Nice, I will order a hamburger for you!",
    "response" : {}
  },
  {
    "id" : 7,
    "question" : "Nice, I will order a hamburger for you!",
    "response" : {}
  },
  {
    "id" : 8,
    "question" : "Ok, I will order the best pizza in town for you",
    "response" : {}
  },
  {
    "id" : 9,
    "question" : "No? Well... stay hungry then",
    "response" : {}
  }
]
```

Each object is Question that is sent to the user along with user response options in response dictionary.<br>
The keys in response dictionary are the options for each question, and the values of the keys are the ids of the
next question object that would be traversed to, as per user input.<br>
The id is the identifier of question object, and is local to a questionaire, a different questionaire can have same question id.


Consider the example:<br>
First query : 
`Are you hungry?`<br>
The next question if the user response if `yes` is `What would you like to eat?` hence, the value for key yes is : 2
<br>And if the user inputs `no` the question in `Ok. Call me when you're hungry.`, indicated by 3.

<H4>Note :</H4> Working json file for demo upload : chat/test_data/demo.json