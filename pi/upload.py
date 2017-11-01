import pysftp
import paramiko
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

def put_with_paramiko(local_file_path):

	try:
		remote_media_dir = local_file_path
		remote_media_dir = os.path.join('/home/jay',remote_media_dir)

		# path_to_key = os.path.join('ssh_key','id_rsa')

		path_to_key = '/Users/meshde/Mehmood/HomeAutomationBackend/pi/ssh_key/id_rsa'


		# Open a transport

		host = "139.59.65.16"
		port = 2222
		transport = paramiko.Transport((host, port))

		# Auth\
		key = paramiko.RSAKey.from_private_key_file(path_to_key)
		print("HERE")
		username = "jay"
		transport.connect(username = username, pkey = key)

		print("****Connection Successful*****")

		# Go!

		sftp = paramiko.SFTPClient.from_transport(transport)

		sftp.put(local_file_path,remote_media_dir)

		print("Successfully uploaded file.")

		sftp.close()
		transport.close()

	except FileNotFoundError:
		print("FileNotFoundError")
		sftp.close()
		transport.close()
