#-*- coding: utf-8 -*-
from gtts import gTTS
import os, time
from pygame import mixer

tts= gTTS(text='펩시 콜라 어디있나요', lang='ko')
tts.save('펩시_콜라_어디있나요.wav')
mixer.init()
mixer.music.load('펩시_콜라_어디있나요.wav')
mixer.music.play()
while mixer.music.get_busy():
    time.sleep(1)

# INSTALL:
# sudo apt-get install python-pymad
# sudo pip3 install --upgrade requests
# sudo pip3 install --upgrade gTTS
# sudo pip3 install pygame