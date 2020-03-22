from pprint import pprint
import os
import ftplib
from tqdm import tqdm
from os import path
import sys

def is_file(ftp, path):
	try:
		ftp.cwd(path)
		return False
	except:
		return True


if path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.py')) == False:
	print('\nConfig file "config.py" missing')
	sys.exit()



import config



print('\nStart synchronization')




for storage in config.config:

	print('\nConnecting to: '+storage['ip'])

	ftp = ftplib.FTP(storage['ip'])
	ftp.login(storage['user'], storage['password'])

	ftp_files = []

	ftp.cwd(storage['ftp_path'])
	ftp.retrlines('NLST', ftp_files.append)



	ftp_files = list(filter(lambda x: x not in ['.', '..'], ftp_files))
	ftp_files = list(filter(lambda path: is_file(ftp, storage['ftp_path'] + path), ftp_files))

	if ftp_files:

		print('\nFTP files:')
		pprint(ftp_files)



		local_files = os.listdir(storage['local_path'])
		if local_files:
			print('\nLocal files:')
			pprint(local_files)
		else:
			print('\nNo local files')




		new_files = list(set(ftp_files) - set(local_files))

		if new_files:
			print('\nNew files:')
			pprint(new_files)
			print('\nDownloading files...')
			for filename in new_files:

				new_local_file = storage['local_path'] + '\\' + filename
				with open( new_local_file, 'wb' ) as file :

					ftp.voidcmd('TYPE I')
					total = ftp.size(storage['ftp_path']+filename)

					with tqdm(total=total) as progress_bar:
						def file_write(data):
							progress_bar.update(len(data))
							file.write(data)

						ftp.retrbinary('RETR %s' % storage['ftp_path']+filename, file_write)

				if os.path.isfile(new_local_file) == True:
					print('File downloaded: ' + filename )
				else:
					print('Error downloading file: ' + filename)
		else:
			print('\nNo new files to download')



		old_files = list(set(local_files) - set(ftp_files))

		if old_files:
			print('\nOld files:')
			pprint(old_files)
			print('\nDeleting files...')
			for filename in old_files:
				old_local_file = storage['local_path'] + '\\' + filename

				if os.path.isfile(old_local_file):
					os.remove(old_local_file)

					if os.path.isfile(old_local_file) == False:
						print('File removed: ' + filename)
		else:
			print('\nNo old files to delete')


	else:
		print('\nNo FTP files')


	ftp.quit()







print('\nEnd of synchronization')