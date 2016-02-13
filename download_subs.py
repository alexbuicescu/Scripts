import sys

from datetime import timedelta

from babelfish import Language
from subliminal import download_best_subtitles, region, save_subtitles, scan_videos

def main(path):
	# configure the cache
	region.configure('dogpile.cache.dbm', arguments={'filename': 'cachefile.dbm'})

	playlist_location = ''

	print 'started to scan for videos'
	# scan for videos newer than 2 weeks and their existing subtitles in a folder
	videos = [v for v in scan_videos(path) ]#if v.age < timedelta(weeks=2)]

	print 'started to download subs'
	# download best subtitles
	subtitles = download_best_subtitles(videos, {Language('eng'), Language('ron')})

	print 'started to save subs'
	# save them to disk, next to the video
	for v in videos:
		print 'save sub: ', v
		save_subtitles(v, subtitles[v])

if __name__ == "__main__":
	if len(sys.argv) >= 2:
		main(sys.argv[1])
	else:
		main('')
# main('/Users/alexbuicescu/Movies/Seriale/Supernatural/S11')