import time
from pprint import pprint
import paramiko
from paramiko.ssh_exception import SSHException


def cisco_get_show_output(
    host, username, password, enable_pass, command, pause=0.5, max_read=100000
):
    with paramiko.SSHClient() as client:
        client.load_system_host_keys()
        try:
            client.connect(
                hostname=host,
                username=username,
                password=password,
                look_for_keys=False,
                allow_agent=False,
                timeout=5,
            )
        except (OSError, SSHException) as error:
            print(error)
        else:
            try:
                ssh = client.invoke_shell()
                ssh.settimeout(5)
                ssh.send("enable\n")
                time.sleep(pause)
                ssh.send(f"{enable_pass}\n")
                time.sleep(pause)
                ssh.send("terminal length 0\n")
                time.sleep(pause)
                ssh.recv(max_read)
                ssh.recv(max_read)

                ssh.send(f"{command}\n")
                time.sleep(pause * 4)
                output = ssh.recv(max_read)
                return output.decode("utf-8").replace("\r\n", "\n")
            except OSError as error:
                print(error)



if __name__ == "__main__":
    out = cisco_get_show_output(
        "192.168.100.1", "cisco", "cisco", "cisco", "sh ip int br", pause=0.3
    )
    pprint(out, width=120)
