# SpotifyApps
Playing with the Spotify API

lots of help with authorization from here: https://github.com/mari-linhares/spotify-flask


# credentials.py 

put this in root directory

CLIENT_ID = ""
CLIENT_SECRET = ""


# deploying to AWS

`pip install awsebcli`

`eb init` to start the eb project

`eb create` to spin up the actual compute resources

`eb ssh` to ssh into the box

Workflow:

```
git add
git commit 
git push
eb deploy
```

Notes:

application MUST BE CALLED `application.py` and must run with `python application.py`. 
There are ways to change this but they are not super intuitive.

`application` object in `application.py` MUST BE CALLED `application` 

if you want to deploy a file to EB (like credentials) but not git, you created a `.ebignore` file that does not list that file

Need a better way to determine the environment and set things like MYHOSTNAME for the callback URI

You don't need to use `virtualenv` but you DO need to have a `requirements.txt`

The directory (not git repo) you run `eb init` from is what it will use

can access the logs by going to the AWS console (e.g. `stdout`)

can set env variables etc with files like in `.ebextensions`

These are good tutorials:

* https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80

