#!/bin/python
import vagrant
from ansible.module_utils.basic import AnsibleModule
from pathlib import Path


def main():
    module_args = dict(
        path=dict(type='str', required=True),
        state=dict(type='str', required=True)
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    result = {}

    if not Path("%s/Vagrantfile" % module.params['path']).is_file():
        module.fail_json(msg="Error: Vagrantfile doesn't exists", **result)

    v = vagrant.Vagrant()

    if module.params['state'] == "started":
        v.up()
        result['status'] = v.status()[0].state
        result['ip'] = v.conf()["HostName"]
        result['host'] = v.conf()["Host"]
        result['port'] = v.conf()["Port"]
        result['key'] = v.conf()["IdentityFile"]
        result['username'] = v.conf()["User"]
        result['RAM size'] = v.ssh(command='free -m').split()[7]
        result['os_name'] = v.ssh(command='cat /etc/*-release').split()[0]
    elif module.params['state'] == "stopped":
        v.halt()
    elif module.params['state'] == "destroyed":
        v.destroy()
    else:
        module.fail_json(msg='This program understand only: started, stopped, destroyed commands', **result)
    result['vm_status'] = v.status()[0].state
    """
    with open('inventory', 'w') as outfile:
        outfile.close()
    """
    module.exit_json(**result)


if __name__ == '__main__':
    main()
