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
 > 1. Installing a local server like xampp: (https://www.apachefriends.org/fr/download.html)
 > 2. Edit the htpd.conf file to get this:
 ```sh
    <IfModule mod_headers.c>
        Header always set Access-Control-Allow-Origin "*"
        Header always set Access-Control-Allow-Headers "Content-Type"
    </IfModule>
 ```
 > 3. Edit the upload.js like this:
 ```sh
        var commande = new FormData();
        commande.append("couleur", "rouge");
        commande.append("pointure", "43");
        // Envoi de l'objet FormData au serveur
        ajaxPost("your url", commande,
            function (reponse) {
                // Affichage dans la console en cas de succès
                console.log("Commande envoyée au serveur");
            }
        );
        var form = document.querySelector("form");
        // Gestion de la soumission du formulaire
        form.addEventListener("submit", function (e) {
            e.preventDefault();
            // Récupération des champs du formulaire dans l'objet FormData
            var data = new FormData(form);
            // Envoi des données du formulaire au serveur
            // La fonction callback est ici vide
            ajaxPost("your url", data, function () {});
        });
 ```

 ### Django
 We use Django to run python scripts on our website.
 > 1. Django is a python framework so you need python (https://www.python.org/downloads/)
 > 2. Open a new terminal and create a virtual environment like this:
 ```sh
    python3 -m venv NameOfEnvironment
  ```
> 3. Activate your environment :
```sh
    NameOfEnvironment\Scripts\activate
```
> 4. Then you need the latest version of pip:
```sh
    python -m pip install --upgrade pip
```
> 5. Finally install django:
```sh
    pip install -r requirements.txt
```
## Author
- **Etienne Legallic**
- **Nathan Martinelli**