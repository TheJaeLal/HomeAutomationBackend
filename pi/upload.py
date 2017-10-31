import pysftp
import os

#local_file_path is going to be of the format.. 'static/videos/filename.mp4'

def put(local_file_path):

	try:
		remote_media_dir = os.path.dirname(local_file_path)

		# path_to_key = os.path.join('ssh_key','id_rsa')

		path_to_key = "ssh_key/id_rsa"

		server = pysftp.Connection(host = "139.59.65.16",username = 'jay', port = 2222, private_key = path_to_key)

		print("****Connection Successful*****")

		print("remote_media_dir = ",remote_media_dir)
		server.cwd(remote_media_dir)

		print("Successful changed directory")
		server.put(local_file_path)

		print("Successfully uploaded file.")

	except FileNotFoundError:
		print("FileNotFoundError")
		server.close()