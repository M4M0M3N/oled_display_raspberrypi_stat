import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess


#Decommentare la riga del vostro display

# 128x32 display I2C:
#disp = Adafruit_SSD1306.SSD1306_128_32(rst=None)

# 128x64 display I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)


# Inizializziamo il display
disp.begin()

# Puliamo il display, non indispensabile
#disp.clear()
#disp.display()

# Disegna il logo all'avvio
image = Image.open('/home/pi/oled_display/logo.ppm').convert('1')
disp.image(image)
disp.display()
time.sleep(2)

# Creiamo un rettandolo nero per disegnarci sopra
# Il colore deve essere a 1 bit
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Ottieni l'oggetto di disegno per disegnare sull'immagine.
draw = ImageDraw.Draw(image)

# Alcune variabili per disegnare piu' semplicemente
padding = -2
top = padding
bottom = height-padding
# Muovi la x per spostare piu' al centro l escritte nel display
x = 0


# Carica il font di default
font = ImageFont.load_default()

# In alternativa, carica un font TTF. Assicurati che il file del carattere .ttf si trovi nella stessa directory dello script Python!
# Li puoi trovare qui: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)



# Disegna una casella piena di nero per cancellare l'immagine.
draw.rectangle((0,0,width,height), outline=0, fill=0)

#Reupero le info del Sistema operativo
cmd = " hostnamectl"
info_OS = subprocess.check_output(cmd, shell = True ).decode('utf-8').split("\n")[:-1]

# eliminiamo le info che non ci servono
info_OS.pop(3)
info_OS.pop(2)
info_OS.pop(1)

for i in range(len(info_OS)):
    
    c=0
    while info_OS[i][c] == ' ':
        c+=1
    
    info1, info2 = info_OS[i][c:].split(':')
    draw.text((x, top+i*16),    f"{info1}", font=font, fill=255)
    draw.text((x, top+i*16+8),    f"{info2}", font=font, fill=255)

disp.image(image)
disp.display()
time.sleep(5)

OS = info_OS[0].split(": ")[-1]
	

while True:

    # Disegna un rettangolo per cancellare le scritte precedenti
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Questi comandi servono per reperire le info del sistema

    cmd = "hostname -I"
    IP = subprocess.check_output(cmd, shell = True ).decode('utf-8').replace(" \n","") 
    
    cmd = "vcgencmd measure_temp"
    TEMP = subprocess.check_output(cmd, shell = True ).decode('utf-8').replace("\n","").split("=")[1]

    cmd = "top -d 0.5 -b -n2 | grep \"Cpu(s)\"|tail -n 1 | awk \'{print $2 + $4}\'"
    CPU = subprocess.check_output(cmd, shell = True ).decode('utf-8').replace("\n","")
    
    cmd = "free -m | awk 'NR==2{printf \"Mem: %.0f%%##%s/%sMB\", $3*100/$2,$3,$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True ).decode('utf-8').replace(" \n","").split("##")
    
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True ).decode('utf-8').replace("\n","")

    # Qui scrivo le informazioni nel display
    riga = 8

    draw.text((x, top),       f"Info rasp", font=font, fill=255)
    draw.text((x, top+riga),  f"{OS}", font=font, fill=255)

    draw.text((x, top+2*riga),    f"CPU: {CPU}%", font=font, fill=255)    
    draw.text((x, top+3*riga),    f"Temperatura {TEMP}",  font=font, fill=255)    
    draw.text((x, top+4*riga),    str(MemUsage[0]),  font=font, fill=255)
    draw.text((x, top+5*riga),    str(MemUsage[1]),  font=font, fill=255)
    draw.text((x, top+6*riga),    f"IP: {IP}",  font=font, fill=255)
    draw.text((x, top+7*riga),    str(Disk),  font=font, fill=255)

    # Qui mando le info nel display per visualizzarle
    disp.image(image)
    disp.display()
    time.sleep(.1)
