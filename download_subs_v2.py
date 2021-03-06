import os
import sys

from datetime import timedelta

from babelfish import Language
from subliminal import download_best_subtitles, region, save_subtitles, scan_videos


def getAllDirs(path):
	dirs_tuples = os.walk(path)
	dirs = [directory[0] for directory in dirs_tuples]
	return dirs


def findExistingPaths():
	paths = {}
	# rw+ so it creates the file for the first time the script is executed
	with open('downloaded_subs.txt', 'rw+') as f:
		data = f.read() or ''
		print 'data:', data
		paths = {sub: True for sub in data.split('\n') or [] if sub}

	return paths


def downloadForFolder(folderPath):
	# configure the cache
	region.configure('dogpile.cache.dbm', arguments={'filename': 'cachefile.dbm'})

	playlist_location = ''

	print 'started to scan for videos in: {}'.format(folderPath)
	# scan for videos newer than 2 weeks and their existing subtitles in a folder
	videos = [v for v in scan_videos(folderPath) ]#if v.age < timedelta(weeks=2)]

	print 'started to download subs'
	# download best subtitles
	subtitles = download_best_subtitles(videos, {Language('eng'), Language('ron')})

	print 'started to save subs'
	# save them to disk, next to the video
	for v in videos:
		print 'save sub:\n-{}\n-{}\n'.format(v, subtitles[v])
		save_subtitles(v, subtitles[v])


def main(path, contains=''):
	if not path:
		path = '/'

	existingPaths = findExistingPaths()
	# print 'existing:', '\n'.join(existingPaths)
	allDirs = getAllDirs(path)
	# print '\nall:', '\n'.join(existingPaths)
	newDirs = [directory for directory in allDirs if not existingPaths.get(directory)]
	# print('found {} new directories:\n{}'.format(len(newDirs), '\n'.join(newDirs)))

	if not newDirs:
		print 'no new directories found'
		return

	if contains:
		contains = contains.lower()
		newDirs = [directory for directory in newDirs if contains in directory.lower()]

	if not newDirs:
		print 'no new directories matching "{}" found'.format(contains.lower())
		return

	user_input = raw_input('found {} new directories:\n{}\n\nContinue? [Y/n] '.format(len(newDirs), '\n'.join(newDirs)))
	user_input = user_input.lower()

	if user_input not in ['', None, 'y', 'yes']:
		exit(-1)
		return

	for directory in newDirs:
		downloadForFolder(directory)
		# pass
	
	with open('downloaded_subs.txt', 'a+') as f:
		f.write('\n'.join(newDirs) + '\n')

if __name__ == "__main__":
	if len(sys.argv) >= 2:
		main(sys.argv[1])
	else:
		main('/')
# main('/Users/alexbuicescu/Movies')
