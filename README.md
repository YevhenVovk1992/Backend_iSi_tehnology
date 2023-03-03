# Simple Messenger
### Test project for the Junior Python position in iSi technology
___
## Content
 - [Technologies](#what-we-used)
 - [Desription](#what-we-do)
 - [Star Project](#how-to-start-project)
 - [Sources](#sources)
___
## What we used?
_Technologies used_: Djando, DRF, Simple JWT,SQLite.

## What we do?
We have developed a messanger. Only authenticated users can work with the service. 
To pass authorization, pass the key-token in the request. Using the Django admin panel, 
you can register a user and get a token for him. <br>
**Paths:**
- [http://127.0.0.1:8000/api/token/](http://127.0.0.1:8000/api/token/) - Get user token
- [http://127.0.0.1:8000/application/thread/](http://127.0.0.1:8000/application/thread/) - Send POST request to create thread
- [http://127.0.0.1:8000/application/thread/id_thread/](http://127.0.0.1:8000/application/thread/<id_thread>/) - Send DELETE request to delete thread. Write ID in the pass.
- [http://127.0.0.1:8000/application/thread/list](http://127.0.0.1:8000/application/thread/list) - Send GET request to get thread list.
- [http://127.0.0.1:8000/application/message/](http://127.0.0.1:8000/application/message/) - Send GET request to get message list for the thread. Specify the parameter "thread" in JSON. 
- [http://127.0.0.1:8000/application/message/](http://127.0.0.1:8000/application/message/) - Send POST request to create message for the thread. Specify the parameter "thread" and "text" in JSON. 
- [http://127.0.0.1:8000/application/message/id_message/status/](http://127.0.0.1:8000/application/message/11/status/) - Send PUT request to set for the message status. Specify the parameter "thread" and "is_read" in JSON.
Write ID of the message in the pass.
- [http://127.0.0.1:8000/application/message/unread/](http://127.0.0.1:8000/application/message/unread/) - Send GET request to get all unread message. Specify the parameter "thread" in JSON. 

2 Django models were developed - 'Thread' and 'Message'. 'Message' model stores messages tied to a thread.
'Thread' establishes a connection between two users. Column 'participants' contains two variables that indicate the ID of the users in the thread.
If the user is not in 'participants' column, he does not have access to messages with other threads.
You can see the structure of the request and the JSON in the file `check_api.http`.

## How to start project?
1. Run `git clone {SSH-link from GitHub}` on your PC;
2. Run `pip install -r requirements.txt`;
3. Create '.env' file and write to it the enviroment variables:
	- SECRET_KEY (Fot example: 'django-insecure-5tj_b9&8y82i5lpeh1cc_3k^rgp4=!ti1wnu7x8!nop0@!281$')
4. Run `python3 manage.py migrate`;
5. Create superuser '`python3 manage.py createsuperuser`; 

## Sources
1. [Django REST framework official](https://www.django-rest-framework.org/)
2. [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html)
