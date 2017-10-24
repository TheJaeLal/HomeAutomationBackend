import pysftp
import os

#local_file_path is going to be of the format.. 'static/videos/filename.mp4'

def put(local_file_path, thread_name):

	try:
		remote_media_dir = os.path.dirname(local_file_path)

		path_to_key = os.path.join('ssh_key','id_rsa')

		server = pysftp.Connection(host = "139.59.65.16",username = 'jay', port = 2222, private_key = path_to_key)

		print(thread_name,"****Connection Successful*****")

		print(thread_name,"remote_media_dir = ",remote_media_dir)
		server.cwd(remote_media_dir)

		print(thread_name,"Successful changed directory")
		server.put(local_file_path)

		print(thread_name,"Successfully uploaded file.")

	except FileNotFoundError:
		print(thread_name,"FileNotFoundError")
		server.close()