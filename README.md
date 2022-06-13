# Oled display raspberrypi stat
Come collegare un display oled 128x64 al raspberry per visualizzare le info
Ho eseguito questa guida usando la versione 10 di raspbian.
La guida funziona anche su retropie

![Anteprima](https://github.com/M4M0M3N/oled_display_raspberrypi_stat/blob/main/immagini/gif.gif?raw=true)

# Per prima cosa abilitiamo il protocollo i2c del raspberry
Andare in raspi-config
> sudo raspi-config

Entrare in Interface Option
attivare i2c

Riavviare il rasp
> sudo reboot

# Collegamento elettrico
Collegare il display come in foto.
Bisogna alimentare il display a 3.3v e non 5v

![schema elettrico](https://github.com/M4M0M3N/oled_display_raspberrypi_stat/blob/main/immagini/schema_elettrico.png?raw=true)

# Installare le librerie e copiare i file
Crea una nuova cartella per tenere i file ordinati, la mia si chiamerà oled_display
> mkdir oled_display

Ora copiaci dentro i dentro i file
- stat.py
- logo.ppm

Li puoi prendere da questa repository

Ora bisogna installare le librerie

Scarichiamo la repository
> git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git

Spostiamoci nella cartella appena creata
> cd Adafruit_Python_SSD1306

Aggiorniamo il sistema
> sudo apt-get update

Installiamo le librerie richieste

Probabilmente queste librerie sono gia installate, ma meglio controllare
> sudo apt install -y python3-dev 

> sudo apt install -y python-smbus 
> 
> sudo apt install -y i2c-tools 

> sudo apt install -y python3-pil 

> sudo apt install -y python3-pip 

> sudo apt install -y python3-setuptools 

> sudo apt install -y python3-rpi.gpio


Installaiamo infine, la libreria per far funzionare il display
> sudo python3 setup.py install

Ora possiamo eliminare la cartella appena scaricata
> cd ..

> sudo rm -rf Adafruit_Python_SSD1306

# Test script
Ora siamo pronti a provare lo script. Spostiamo dentro oled_display
> cd oled_display
 
e digitiamo 
> python3 stat.py

per farlo partire

Se vi esce un errore simile a questo
> ModuleNotFoundError: No module named 'Adafruit_BBIO'

Basta fare
> pip3 install Adafruit_BBIO

Se invece vi dice che non trova un file, bisogna che modifichiate il file stat.py
Per farlo scrivete 
> nano stat.py

E alla riga 30
> image = Image.open('/home/pi/oled_display/logo.ppm').convert('1')

Modificatela con il path dove si trova il vostro script
> image = Image.open('/home/pi/cartella1/cartella2/cartella3/logo.ppm').convert('1')

Ora possiamo vedere il display che ci mostra le informazioni.
Per stoppare lo script premiamo
> ctrl-c

# Auto run dello script
Ora dobbiamo dire al rasp di avviare lo script ad ogni boot.
Scriviamo
> sudo nano /lib/systemd/system/oled_display.service

Dentro possiamo mettere questo
```python
[Unit]
Description=Oled display info i2c
[Service]
ExecStart=/usr/bin/python3 /home/oled_display/stats.py
Restart=always
User=pi
[Install]
WantedBy=multi-user.target
```

Ora proviamo a far partire il systemctl
> sudo systemctl start oled_display.service

Possiamo cambiare start con:
- restart per riavviare il processo
- stop per fermarlo

Ora diciamo al raspberry di avviare questo systemctl al boot del sistema operativo
> sudo systemctl enable oled_display.service

Ora, se riavviamo, possiamo vedere che il display si accende al boot del raspberry
