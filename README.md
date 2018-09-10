# Scripts

### Jumping over words in intellij's terminal is not working. Add this to ```~/.inputrc```:
```bash
"\e\e[C": forward-word
"\e\e[D": backward-word
```

### download_subs_v2.py
Looks for all folders/videos in given path and if the folder/video was not "searched" until now, then look for subtitles there. It saves "searched" folders in ```downloaded_subs.txt```.

### download_subs_mp4.py
Same as ```download_sub_v2.py``` only that it also converts videos to **mp4** and copies them to a separate folder (it also copies the english subtitle).
