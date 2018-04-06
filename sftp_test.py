"""A simple application to test the speed of an sftp connection"""

import datetime
import logging
import os
import sys

import paramiko


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
log_level = os.environ.get("LOG_LEVEL", "INFO")
if log_level == 'DEBUG':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)


def ssh_login(host, user, path_to_key):
    """Returns an active ssh client"""
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
    key = paramiko.RSAKey.from_private_key_file(path_to_key)
    logger.info("Attempting SSH login")
    try:
        logger.info("Connecting to remote SFTP server")
        ssh_client.connect(host, username=user, pkey=key)
        logger.info("Connection established")
        return ssh_client
    except:
        logger.info("Unexpected error:", sys.exc_info()[0])
        raise

def main():
    """The main function"""
    host = os.environ.get("HOST")
    user = os.environ.get("USER")
    path_to_key = os.environ.get("PATH_TO_KEY")
    remote_directory_path = os.environ.get("REMOTE_DIRECTORY_PATH")
    local_directory_path = os.environ.get("LOCAL_DIRECTORY_PATH")
    num_files_to_skip = os.environ.get("NUM_FILES_TO_SKIP")
    num_files_to_pull = os.environ.get("NUM_FILES_TO_PULL")

    ssh_client = ssh_login(host, user, path_to_key)
    sftp = ssh_client.open_sftp()

    sftp.chdir(remote_directory_path)
    sftp_source_dir_list = sftp.listdir()
    # This will be a list of all files in the directory

    num_of_files = len(sftp_source_dir_list)
    logger.info("There are %s files in remote directory", num_of_files)

    results = []
    total_filesize = 0
    total_time = datetime.timedelta(seconds=0)
    index = num_files_to_skip
    while index < num_files_to_skip + num_files_to_pull:
        logger.debug("Pulling file: %s", sftp_source_dir_list[index])
        target = os.path.join(local_directory_path, sftp_source_dir_list[index])

        start_time = datetime.datetime.now()
        sftp.get(sftp_source_dir_list[index], target)
        elapsed_time = datetime.datetime.now() - start_time

        result = {
            'filename': sftp_source_dir_list[index],
            'filesize': os.path.getsize(target),
            'time': elapsed_time
        }
        results.append(result)
        total_filesize += result['filesize']
        total_time += elapsed_time
        logger.info("File: %s Size: %s Time taken: %s", sftp_source_dir_list[index], filesize, elapsed_time)
        index += 1

    total_filesize_in_megabytes = total_filesize / float(1000000)
    total_time_in_seconds = str(total_time.seconds) + '.' + str(total_time.microseconds)
    logger.info("Transferred %sMB in %s seconds", total_filesize_in_megabytes, total_time_in_seconds)

if __name__ == "__main__":
	main()
