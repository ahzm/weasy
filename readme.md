# Project configuration

[TOC]

## 1. Dependency tools

Versions:

- node 12.18.3
- npm 6.14.6
- react 17.0.2
- python 3.7: 
  - Librairies to install: requests, networkx
- Tomcat 8.5

### 1). Install node 

Download link: https://nodejs.org/fr/download/current/

### 2). Install React

 npm install -g create-react-app

### 3). install python 

Can be installed via 3.1 or 3.2

3.1) Python >= 3.7

Download link: https://www.python.org/downloads/

pip install requests

pip install networkx

3.2) install Anaconda (Python >=3.7)

Download link: https://www.anaconda.com/products/individual

conda install requests

conda install networkx

### 4). install tomcat

Download link: https://tomcat.apache.org/download-80.cgi

Deploy server/transformation.war project to tomcat



## 2. Deploy the project locally

### 1) Clone

git clone https://github.com/ahzm/weasy.git

### 2) Deploy the project

2.1)Go to the project file:  cd weasy 

Execute the command:  **npm install**

2.2) Go to the project file: cd client 

Execute the command: **npm install**

2.3) Start tomcat

tomcat/bin/startup.bat

### 3) Project launch

Enter the project and execute the command: **npm start**
