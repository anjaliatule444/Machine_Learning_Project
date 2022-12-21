# Machine_Learning_Project
Machine Learning End To End Project

Application URL
```
http://mlregressionflask.herokuapp.com/
```

## Software and Account Requirement
Requirements
1.Github Account
2.Heroku Account
3.Visual Studio Code IDE
4.Git CLI
5.GIT Documentation- https://git-scm.com/docs/gittutorial


Creating Conda Environment
```
conda create -p venv python==3.7 -y
```

Activate conda environment
```
conda activate venv/
OR
source activate venv/
```

To Add files to git
```
git add .
OR
git add <file_name>
```

Note: To ignore file or folder from git we can write name of file/folder in .gitignore file

To check the git status
```
git status
```

To check all version maintained by git
```
git log
```

To create version/commit all changes by git
```
git commit -m "message"
```

To send version/changes to github
```
git push origin main
```

To check remote url
```
git remote -v
```

To setup CI/CD pipeline in heroku we need 3 information
```
HEROKU_EMAIL = anjaliaatule444@gmail.com
HEROKU_API_KEY = <>
HEROKU_APP_NAME = simple-hello-world-flask
```

BUILD DOCKER IMAGE
```
docker build -t <image_name>:<tagname> .
```

Note: Image name for docker must be lowercase

To list docker image
```
docker images
```

Run docker image
```
docker run -p 5000:5000 -e PORT=5000 f8c749e73678
```

To check running container in docker
```
docker ps
```

To remove docker Image
```
docker image rm IMAGE ml-project 
```

To stop docker conatiner
```
docker stop <container_id>
```

Once setup file is created run 
```
python setup.py install (This will install all dependencies   )
```

Install Ipynb kernel
```
pip install ipykernel
```