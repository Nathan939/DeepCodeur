#!/usr/bin/python

print ('Content-type: text/html')
print (
    <html>

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
            
            <script>
        var startRecordingButton = document.getElementById("startRecordingButton");
        var stopRecordingButton = document.getElementById("stopRecordingButton");
        var playButton = document.getElementById("playButton");
        var downloadButton = document.getElementById("downloadButton");


        var leftchannel = [];
        var rightchannel = [];
        var recorder = null;
        var recordingLength = 0;
        var volume = null;
        var mediaStream = null;
        var sampleRate = 44100;
        var context = null;
        var blob = null;

        startRecordingButton.addEventListener("click", function () {
            // Initialize recorder
            navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
            navigator.getUserMedia(
            {
                audio: true
            },
            function (e) {
                console.log("user consent");

                // creates the audio context
                window.AudioContext = window.AudioContext || window.webkitAudioContext;
                context = new AudioContext();

                // creates an audio node from the microphone incoming stream
                mediaStream = context.createMediaStreamSource(e);

                // https://developer.mozilla.org/en-US/docs/Web/API/AudioContext/createScriptProcessor
                // bufferSize: the onaudioprocess event is called when the buffer is full
                var bufferSize = 2048;
                var numberOfInputChannels = 2;
                var numberOfOutputChannels = 2;
                if (context.createScriptProcessor) {
                    recorder = context.createScriptProcessor(bufferSize, numberOfInputChannels, numberOfOutputChannels);
                } else {
                    recorder = context.createJavaScriptNode(bufferSize, numberOfInputChannels, numberOfOutputChannels);
                }

                recorder.onaudioprocess = function (e) {
                    leftchannel.push(new Float32Array(e.inputBuffer.getChannelData(0)));
                    rightchannel.push(new Float32Array(e.inputBuffer.getChannelData(1)));
                    recordingLength += bufferSize;
                }

                // we connect the recorder
                mediaStream.connect(recorder);
                recorder.connect(context.destination);
            },
                        function (e) {
                            console.error(e);
                        });
        });

        stopRecordingButton.addEventListener("click", function () {

            // stop recording
            recorder.disconnect(context.destination);
            mediaStream.disconnect(recorder);

            // we flat the left and right channels down
            // Float32Array[] => Float32Array
            var leftBuffer = flattenArray(leftchannel, recordingLength);
            var rightBuffer = flattenArray(rightchannel, recordingLength);
            // we interleave both channels together
            // [left[0],right[0],left[1],right[1],...]
            var interleaved = interleave(leftBuffer, rightBuffer);

            // we create our wav file
            var buffer = new ArrayBuffer(44 + interleaved.length * 2);
            var view = new DataView(buffer);

            // RIFF chunk descriptor
            writeUTFBytes(view, 0, 'RIFF');
            view.setUint32(4, 44 + interleaved.length * 2, true);
            writeUTFBytes(view, 8, 'WAVE');
            // FMT sub-chunk
            writeUTFBytes(view, 12, 'fmt ');
            view.setUint32(16, 16, true); // chunkSize
            view.setUint16(20, 1, true); // wFormatTag
            view.setUint16(22, 2, true); // wChannels: stereo (2 channels)
            view.setUint32(24, sampleRate, true); // dwSamplesPerSec
            view.setUint32(28, sampleRate * 4, true); // dwAvgBytesPerSec
            view.setUint16(32, 4, true); // wBlockAlign
            view.setUint16(34, 16, true); // wBitsPerSample
            // data sub-chunk
            writeUTFBytes(view, 36, 'data');
            view.setUint32(40, interleaved.length * 2, true);

            // write the PCM samples
            var index = 44;
            var volume = 1;
            for (var i = 0; i < interleaved.length; i++) {
                view.setInt16(index, interleaved[i] * (0x7FFF * volume), true);
                index += 2;
            }

            // our final blob
            blob = new Blob([view], { type: 'audio/wav' });
        });

        playButton.addEventListener("click", function () {
            if (blob == null) {
                return;
            }

            var url = window.URL.createObjectURL(blob);
            var audio = new Audio(url);
            audio.play();
        });

        downloadButton.addEventListener("click", function () {
            if (blob == null) {
                return;
            }

            var url = URL.createObjectURL(blob);

            var a = document.createElement("a");
            document.body.appendChild(a);
            a.style = "display: none";
            a.href = url;
            a.download = "sample.wav";
            a.click();
            window.URL.revokeObjectURL(url);
        });

        function flattenArray(channelBuffer, recordingLength) {
            var result = new Float32Array(recordingLength);
            var offset = 0;
            for (var i = 0; i < channelBuffer.length; i++) {
                var buffer = channelBuffer[i];
                result.set(buffer, offset);
                offset += buffer.length;
            }
            return result;
        }

        function interleave(leftChannel, rightChannel) {
            var length = leftChannel.length + rightChannel.length;
            var result = new Float32Array(length);

            var inputIndex = 0;

            for (var index = 0; index < length;) {
                result[index++] = leftChannel[inputIndex];
                result[index++] = rightChannel[inputIndex];
                inputIndex++;
            }
            return result;
        }

        function writeUTFBytes(view, offset, string) {
            for (var i = 0; i < string.length; i++) {
                view.setUint8(offset + i, string.charCodeAt(i));
            }
        }

    </script>
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


</html>
)


#!/usr/bin/env python3

import speech_recognition as sr

# obtain path to "english.wav" in the same folder as this script
from os import path
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "english.wav")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "french.aiff")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "chinese.flac")

# use the audio file as the audio source
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)  # read the entire audio file

# recognize speech using Sphinx
try:
    print("Sphinx thinks you said " + r.recognize_sphinx(audio))
except sr.UnknownValueError:
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))

# recognize speech using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

# recognize speech using Google Cloud Speech
GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""INSERT THE CONTENTS OF THE GOOGLE CLOUD SPEECH JSON CREDENTIALS FILE HERE"""
try:
    print("Google Cloud Speech thinks you said " + r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
except sr.UnknownValueError:
    print("Google Cloud Speech could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Cloud Speech service; {0}".format(e))

# recognize speech using Wit.ai
WIT_AI_KEY = "INSERT WIT.AI API KEY HERE"  # Wit.ai keys are 32-character uppercase alphanumeric strings
try:
    print("Wit.ai thinks you said " + r.recognize_wit(audio, key=WIT_AI_KEY))
except sr.UnknownValueError:
    print("Wit.ai could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Wit.ai service; {0}".format(e))

# recognize speech using Microsoft Azure Speech
AZURE_SPEECH_KEY = "INSERT AZURE SPEECH API KEY HERE"  # Microsoft Speech API keys 32-character lowercase hexadecimal strings
try:
    print("Microsoft Azure Speech thinks you said " + r.recognize_azure(audio, key=AZURE_SPEECH_KEY))
except sr.UnknownValueError:
    print("Microsoft Azure Speech could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Microsoft Azure Speech service; {0}".format(e))

# recognize speech using Microsoft Bing Voice Recognition
BING_KEY = "INSERT BING API KEY HERE"  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
try:
    print("Microsoft Bing Voice Recognition thinks you said " + r.recognize_bing(audio, key=BING_KEY))
except sr.UnknownValueError:
    print("Microsoft Bing Voice Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))

# recognize speech using Houndify
HOUNDIFY_CLIENT_ID = "INSERT HOUNDIFY CLIENT ID HERE"  # Houndify client IDs are Base64-encoded strings
HOUNDIFY_CLIENT_KEY = "INSERT HOUNDIFY CLIENT KEY HERE"  # Houndify client keys are Base64-encoded strings
try:
    print("Houndify thinks you said " + r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY))
except sr.UnknownValueError:
    print("Houndify could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Houndify service; {0}".format(e))

# recognize speech using IBM Speech to Text
IBM_USERNAME = "INSERT IBM SPEECH TO TEXT USERNAME HERE"  # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
IBM_PASSWORD = "INSERT IBM SPEECH TO TEXT PASSWORD HERE"  # IBM Speech to Text passwords are mixed-case alphanumeric strings
try:
    print("IBM Speech to Text thinks you said " + r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD))
except sr.UnknownValueError:
    print("IBM Speech to Text could not understand audio")
except sr.RequestError as e:
    print("Could not request results from IBM Speech to Text service; {0}".format(e))