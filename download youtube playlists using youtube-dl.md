1. ### Install pip, ffmpeg:
  
  __macOS:__
  ```
  sudo easy_install pip
  brew install ffmpeg
  ```
  
  __Ubuntu:__
  ```bash
  sudo apt-get update
  sudo apt-get -y install python-pip
  sudo apt-get -y install ffmpeg
  ```
  
  ### Install youtube-dl (more info [here](https://github.com/rg3/youtube-dl/blob/master/README.md#how-do-i-update-youtube-dl)):
  ```bash
  . env/bin/activate
  pip install youtube-dl
  ```

### Use youtube-dl:
1. For audio only (`-x` option):
    ```bash
    cd my/path/to/music/folder
    youtube-dl -i --yes-playlist -x -f bestaudio --prefer-ffmpeg --audio-format "mp3" "url_here"
    ```
1. For videos (default is `bestvideo+bestaudio` for format):
    ```bash
    youtube-dl -i --yes-playlist "url_here"
    ```
