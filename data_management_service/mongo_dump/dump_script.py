import subprocess

# Define the container and local file paths
container_name = "065fa5549f0e"
dump_file_path = "/tmp/dump.tar.gz"
local_file_path = "./dump/dump.tar.gz"

# Execute mongodump command within the container
dump_command = (
    f"docker exec {container_name} mongodump --archive={dump_file_path} --gzip"
)
subprocess.run(dump_command, shell=True, check=True)

# Copy the dump file from the container to the local machine
copy_command = f"docker cp {container_name}:{dump_file_path} {local_file_path}"
subprocess.run(copy_command, shell=True, check=True)

print("Database dump created and copied successfully.")
