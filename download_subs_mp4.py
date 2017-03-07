import os
import os.path
import sys
import subprocess
from shutil import copyfile

from datetime import timedelta

from babelfish import Language
from subliminal import download_best_subtitles, region, save_subtitles, scan_videos


ERRORS = []
DOWNLOADED = []
newMovies = []

CUSTOM_MP4_FOLDER_SUFFIX = 'buicescu mp4'

# os.path.exists(file_path)

def getMP4FileName(fileName):
	# path/to/movie.mkv => movie.mkv
	movieFileName = os.path.basename(fileName)
	movieFileNameStripped = movieFileName
	
	if '.' in movieFileName:
		# get the name until last ".": path/to/movie.mkv => path/to/movie
		movieFileNameStripped = ''.join(movieFileName[:movieFileName.rfind('.')])

	global CUSTOM_MP4_FOLDER_SUFFIX
	# path/to/movie.mkv => path/to
	parentDirectory = os.path.abspath(os.path.join(fileName, os.pardir))
	mp4DirectoryName = '{}-{}'.format(parentDirectory, CUSTOM_MP4_FOLDER_SUFFIX)
	
	# path/to/movie.mkv => path/to-buicescu mp4/movie.mp4
	mp4FilePath = os.path.join(mp4DirectoryName, '{}.mp4'.format(movieFileNameStripped))

	if not os.path.exists(mp4DirectoryName):
		os.makedirs(mp4DirectoryName)

	# path/to/movie.mkv => path/to-buicescu mp4/movie.mp4, path/to/movie.mkv => path/to/movie
	return mp4FilePath, os.path.join(parentDirectory, movieFileNameStripped)

def convertToMP4(fileName):
	if '.' not in fileName:
		isMp4 = False
	else:
		isMp4 = ''.join(fileName[fileName.rfind('.')+1:]) == 'mp4'

	mp4FilePath, movieFileNameStripped = getMP4FileName(fileName)
	if not os.path.exists(mp4FilePath):
		# if the movie is not mp4, then convert it
		if not isMp4:
			# -r 60 => force 60 FPS
			try:
				o = subprocess.check_output(
					""" \
					ffmpeg \
					-i "{}" \
					-codec copy "{}" \
					-r 60 \
					""".format(fileName, mp4FilePath),
					stderr=subprocess.STDOUT,
					shell=True
				)
			except subprocess.CalledProcessError as ex:
				o = ex.output
				global ERRORS
				ERRORS.append({'file': fileName, 'error': o})
				return False
		# if the movie is mp4, just copy it to the new folder
		else:
			copyfile(fileName, mp4FilePath)

	# make the subtitle the same name as the movie
	if os.path.exists('{}.en.srt'.format(movieFileNameStripped)):
		copyfile('{}.en.srt'.format(movieFileNameStripped), '{}.srt'.format(mp4FilePath[:-4]))

	return True


def getAllDirs(path):
	dirs_tuples = os.walk(path)
	dirs = [directory[0] for directory in dirs_tuples if not directory[0].endswith(CUSTOM_MP4_FOLDER_SUFFIX)]
	return dirs


def findExistingPaths():
	paths = {}
	# rw+ so it creates the file for the first time the script is executed
	with open('downloaded_subs.txt', 'rw+') as f:
		data = f.read() or ''
		print 'data:', data
		paths = {sub: True for sub in data.split('\n') or [] if sub}

	return paths


def downloadForFolder(folderPath, existingPaths, directoryIndex=0, directoryLength=0):
	playlist_location = ''
	global newMovies

	print 'started to scan for videos in: {}'.format(folderPath)
	# scan for videos newer than 2 weeks and their existing subtitles in a folder
	videos = [v for v in scan_videos(folderPath) if not existingPaths.get(v.name) and v.name not in newMovies and not os.path.abspath(os.path.join(v.name, os.pardir)).endswith(CUSTOM_MP4_FOLDER_SUFFIX)]#if v.age < timedelta(weeks=2)]

	if not videos:
		print 'no new videos found\n'

	print 'started to download subs: ', [v.name for v in videos]
	# download best subtitles
	subtitles = download_best_subtitles(videos, {Language('eng'), Language('ron')})

	print 'started to save subs'
	# save them to disk, next to the video
	for index, v in enumerate(videos):
		print 'save sub for:\n{}/{}(videos), {}/{}(directory) - {}\n\n'.format(
			index + 1,
			len(videos),
			directoryIndex + 1,
			directoryLength,
			v.name
		)
		newMovies.append(v.name)
		save_subtitles(v, subtitles[v])
		convertToMP4(v.name)


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
		print 'looking for videos'
		# if we didn't find anything new, then look for videos in the given folder
		newDirs.append(path)

	if contains:
		contains = contains.lower()
		newDirs = [directory for directory in newDirs if contains in directory.lower()]

	if not newDirs:
		print 'no new directories matching "{}" found'.format(contains.lower())
		print 'looking for videos'
		# if we didn't find anything new, then look for videos in the given folder
		newDirs.append(path)
	else:
		user_input = raw_input('found {} new directories:\n{}\n\nContinue? [Y/n] '.format(len(newDirs), '\n'.join(newDirs)))
		user_input = user_input.lower()
		if user_input not in ['', None, 'y', 'yes']:
			exit(-1)
			return

	# configure the cache
	region.configure('dogpile.cache.dbm', arguments={'filename': 'cachefile.dbm'})

	for index, directory in enumerate(newDirs):
		downloadForFolder(directory, existingPaths, index, len(newDirs))
		# pass
	
	with open('downloaded_subs.txt', 'a+') as f:
		newDirs = [d for d in newDirs if not existingPaths.get(d)]
		if newDirs:
			f.write('\n'.join(newDirs) + '\n')
		global newMovies
		if newMovies:
			f.write('\n'.join(newMovies) + '\n')

	global ERRORS
	if ERRORS:
		import json
		print 'ERRORS:\n', json.dumps(ERRORS)

if __name__ == "__main__":
	if len(sys.argv) >= 2:
		main(sys.argv[1])
	else:
		main('/')
# main('/Users/alexbuicescu/Movies')
