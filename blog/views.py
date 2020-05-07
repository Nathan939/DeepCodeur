from django.shortcuts import render
from django.template import loader

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

from datetime import datetime
from django.shortcuts import render

def index(request):
    template = loader.get_template('blog/index.html')
    return HttpResponse(template.render(request=request))

def date_actuelle(request):
    return render(request, 'blog/date.html', {'date': datetime.now()})


def addition(request, nombre1, nombre2):    
    total = nombre1 + nombre2

    # Retourne nombre1, nombre2 et la somme des deux au tpl
    return render(request, 'blog/addition.html', locals())

def home(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    return HttpResponse("""
        <head>
    
        <title>DeepCodeur</title>
        <link rel="icon" type="image/png" href="image/RedAndBlack.ico" />
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
        <link href='http://fonts.googleapis.com/css?family=Lato' rel='stylesheet' type='text/css'>
        <link rel="stylesheet" href="DeepCodeur.css">
        <script src="script.js"></script>
    </head>
    
   
    
    <body data-spy="scroll" data-target=".navbar" data-offset="60">
        

        <header id="header">
            <nav class="navbar navbar-default navbar-fixed-top">
                <div class="pascontainer">
                    <div class="navbar-header">
                        <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
                             <span class="icon-bar"></span>
                             <span class="icon-bar"></span>
                             <span class="icon-bar"></span>
                        </button>
                    </div>
                    <div class="collapse navbar-collapse" id="myNavbar">
                        <img src="image/RedAndBlack.png" id="logo">
                        <h1><span class="orange">[</span>Deep Codeur<span class="orange">]</span></h1>
                        <ul id="features">
                            <li><a href="#newsletter">Newsletter</a></li>
                            <li><a href="#experience">A propos</a></li>
                            <li><a href="#contact">Contact</a></li>
                        </ul>
                    </div>
                </div>
            </nav>
     
        </header>
       

        </nav>
        
        <section id="main-image">
            <div class="wrapper">
                <form>
                    <h2>Dévellopez votre <br>site web sur mesure<br><strong>A l'aide de votre voix</strong></h2>
                <img src="image/FlecheBasAlpha.png" id="micro" class="button-1">
                <button id="startRecordingButton">Start recording</button>
                <button id="stopRecordingButton">Stop recording</button>
                <input type="submit" value="upload" id="upload">
            
        
                <script src="ajax.js"></script>
                <script src="upload.js"></script>
            

                </form>
            </div>
            <div id="film">
                <iframe frameborder="0"></iframe>
            <div>
        </section>
        

        <section id="experience">

            <section id="oc">
                <h3>Qui est le plus fort ?</h3>
            <form>
                <p>
                    <input type="radio" name="plusFort" id="elephant" value="ELE" checked>
                    <label for="elephant">L'éléphant</label>
                    <br>
                    <input type="radio" name="plusFort" id="rhinoceros" value="RHI">
                    <label for="rhinoceros">Le rhinocéros</label>
                    <br>
                    <input type="radio" name="plusFort" id="hippopotame" value="HIP">
                    <label for="hippopotame">L'hippopotame</label>
                    <br>
                </p>
                <p>
                    <label for="nom">Votre nom</label> :
                    <input type="text" name="nom" id="nom" required>
                </p>

                <input type="submit" value="Votez">
            </form>

            <script src="ajax.js"></script>
            <script src="upload.js"></script>
        </section>
        
            <div class="pascontainer">
                <div class="white-divider"></div>
                <div class="heading">
                </div>
                <ul class="timeline">
                    <li>
                        <div class="timeline-badge"><span class="glyphicon glyphicon-briefcase"></span></div>
                        <div class="timeline-panel-container">
                            <div class="timeline-panel">
                                <div class="timeline-heading">
                                    <h3>PARLER</h3>
                                    <h4>Reconnaissance vocale</h4>
                                    <p class="text-muted"><small class="glyphicon glyphicon-time"></small> 2013-2015</p>
                                </div>
                                <div class="timeline-body">
                                    <p>Grace a la reconnaissance vocale, de simples motset vos idées prennent vie</p>
                                    <p>Laissez libre court a votre imagination</p>
                                </div>
                            </div>
                        </div>
                    </li>
                    <li>
                        <div class="timeline-badge"><span class="glyphicon glyphicon-briefcase"></span></div>
                        <div class="timeline-panel-container-inverted">
                            <div class="timeline-panel">
                                <div class="timeline-heading">
                                    <h3>REGARDER</h3>
                                    <h4>Rendu visuel</h4>
                                    <p class="text-muted"><small class="glyphicon glyphicon-time"></small> 2010-2013</p>
                                </div>
                                <div class="timeline-body">
                                    <p>Le rendu visuel vous permet de visualiser le rendu en direct</p>
                                    <p>Le site web se construit sous vos yeux</p>
                                </div>
                            </div>
                        </div>
                    </li>
                    <li>
                        <div class="timeline-badge"><span class="glyphicon glyphicon-briefcase"></span></div>
                        <div class="timeline-panel-container">
                            <div class="timeline-panel">
                                <div class="timeline-heading">
                                    <h3>AJUSTER</h3>
                                    <h4>Technologie d'ajustement</h4>
                                    <p class="text-muted"><small class="glyphicon glyphicon-time"></small> 2007-2010</p>
                                </div>
                                <div class="timeline-body">
                                    <p>Grace a la mémoir a court thermes, ajustez sans tout recommencer</p>
                                    <p>Gagnez du temps et construisez votre site pas à pas</p>
                                </div>
                            </div>
                        </div>
                    </li>
                
                </ul>
            </div>
            
        </section>
        
                
        <section id="education">
            <div class="container">
                 <div class="red-divider"></div>
                <div class="row">
                    <div class="col-sm-6">
                        <div class="education-block">
                            <h5>2002 - 2006</h5>
                            <span class="glyphicon glyphicon-education"></span>
                            <h3>Sevice disponible 24/24 7j/7</h3>
                            <h4>Création de site a tout moment</h4>
                            <div class="red-divider"></div>
                            <p>Site créer en 5 min</p>
                            <p>Opérationnel a tout heure du jour et de la nuit</p>
                        </div>
                    </div>
                     <div class="col-sm-6">
                         <div class="education-block">
                            <h5>2007</h5>
                            <span class="glyphicon glyphicon-education"></span>
                            <h3>Une ingénérie a votre service</h3>
                            <h4>Développement online en direct</h4>
                            <div class="red-divider"></div>
                            <p>HTML/CSS, Javascript, JQuery</p>
                            <p>Responsive Design</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        
        <section id="recommandations">
            <div class="pascontainer">
                <div class="red-divider"></div>
                <div id="myCarousel" class="carousel slide text-center" data-ride="carousel">
                    <ol class="carousel-indicators">
                         <li data-target="#myCarousel" data-slide-to="0" class="active"></li>
                         <li data-target="#myCarousel" data-slide-to="1"></li>
                         <li data-target="#myCarousel" data-slide-to="2"></li>  
                    </ol>
                    <div class="carousel-inner" role="listbox">
                        <div class="item active">
                            <h3>"Merci pour tout, vous m'avez fait gagner un temps précieux"</h3>
                            <h4>Testeur anonyme</h4>       
                        </div>
                          <div class="item">
                            <h3>"La technologie la plus utile que j'ai essayé"</h3>
                            <h4>Testeur anonyme</h4>       
                        </div>
                          <div class="item">
                            <h3>"Vous evitez de nous apprendre a coder merci pour tout !"</h3>
                            <h4>Testeur anonyme</h4>       
                        </div>
                    </div>
                    <a class="left carousel-control" href="#myCarousel" data-slide="prev" role="button">
                        <span class="glyphicon glyphicon-chevron-left"></span>
                    </a>
                    <a class="right carousel-control" href="#myCarousel" data-slide="next" role="button">
                        <span class="glyphicon glyphicon-chevron-right"></span>
                    </a>
                
                </div>
            
            </div>
        
        
        </section>
        
        
        <section id="contact">
            <div class="wrapper">
                
                <h3>Contactez-nous</h3>
                
                <form>
                    <label for="name">Nom</label>
                    <input type="text" id="name" placeholder="Votre nom">
                    
                    <label for="email">Email</label>
                    <input type="text" id="email" placeholder="Votre email">
                    
                    <input type="submit" value="OK" class="button-3">
                </form>
            
            </div>
            <div class="wrapper" id="newsletter">
                
                <h3>Newsletter</h3>
                
                <form>
                    <label for="email">Email</label>
                    <input type="text" id="email" placeholder="Votre email">
                    
                    <input type="submit" value="OK" class="button-3">
                </form>
            
            </div>
        </section>
        
        
        
        <footer>
            <div class="wrapper">
                <h1><span class="orange">[</span>Deep Codeur<span class="orange">]</span></h1>
                <div class="copyrigth">Copyright © 2020. Tous droits réservés.</div>
                <a href="#header">
                    <span id="up" class="glyphicon glyphicon-chevron-up"></span>
                </a>
            </div>
        </footer>
    </body>
    """)    