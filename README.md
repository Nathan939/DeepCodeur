**Note**
> We are 2 young developers and we are in the middle of our apprenticeship, so we apologize in advance for the quality of the code. We do our best to improve it as we go along.

## Introduction
Deep Codeur is an open source automatic development project. It doesn't need anything to work, just a button and your voice...

You just have to support and describe your website project.

### Why?

> 1. If you don't know how to code it's always frustrating to see that you have to have some knowledge to start your projects. That's why we decided to create an artificial intelligence doing the work for you.
> 2. With this generic structure, everyone can create their own web-sites and share them with others.
> 3. Open source is wonderfull.

### What is the repository for ?
> This repository contains the following nodes of DeepCodeur:
> - All project files

### What DeepCodeur able to do ?
> Today, DeepCodeur is just a web-site but in the future he'll be capable of much more.

## Getting Started
### Local serveur
 To use the service you need a local serveur and modify the httpd.conf file like this:
 <IfModule mod_headers.c>
	# Accept cross-domain requests
	Header always set Access-Control-Allow-Origin "*"
	Header always set Access-Control-Allow-Headers "Content-Type"
</IfModule>

It is also necessary to modify the upload.js file by replacing the urls by your own urls.

### Django
You need to download django by: 
pip install -r requirements.txt

## Author
**Etienne Legallic**
**Nathan Martinelli**