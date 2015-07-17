#install eyed3:
#pip install eyed3 --allow-external eyed3 --allow-unverified eyed3

import os
import eyed3

folder = raw_input('C:\Users\Alexandru\Desktop\Music\Owl City')
files = os.listdir(folder) # This will give us a list of all of the MP3s in that folder
artist = folder.split('\\')[-1]

print artist

# for x in files:
#     mp3 = eyed3.load(folder + '\\' + x) # Loads each and every MP3
#     mp3.tag.artist = unicode(artist, "UTF-8") # Sets the "artist" tag to the artist name 
#     mp3.tag.save() # Saves tag