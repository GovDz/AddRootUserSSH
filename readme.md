# SSH User Addition with Root Permissions

This Python script connects to a list of SSH servers, checks their status, and adds a new user with root permissions. If the 'sudo' group does not exist on your system, it uses the 'root' group.

## Prerequisites

- [paramiko](https://www.paramiko.org/) library: Install it using `pip install paramiko`
- [sshpass](https://linux.die.net/man/1/sshpass): Install it on your system.

## Usage

```bash
python script.py <ssh_list_file> <new_user> <new_user_password>
