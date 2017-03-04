from kickstartBackend import db, pageGenerator
import uuid

DATABASE_PATH = '/tmp/ksdb.sqlite'

def test_write():
    """Not to be used in production. Test code for this module."""
    import os
    #os.remove(DATABASE_PATH)
    db.createdb()
    data1 = {
        'id': str(uuid.uuid4()),
        'order': 1,
        'done': 0,
        'net-hostname': 'host1.test.lab',
        'net-type': 'static',
        'net-ip': '10.0.0.1',
        'net-netmask': '255.255.255.0',
        'net-gateway': '10.0.0.254',
        'net-nameserver': '8.8.8.8,8.8.4.4',
        'root-password': 'geencryptrootwachtwoord',
        'user-name': 'admin',
        'user-gecos': 'Administrator',
        'user-groups': 'wheel,anderegroep',
        'user-password': 'geencryptuserpassword'
    }
    db.write_host(data1)
    data2 = {
        'id': str(uuid.uuid4()),
        'order': 2,
        'done': 1,
        'net-hostname': 'host2.test.lab',
        'net-type': 'static',
        'net-ip': '10.0.0.2',
        'net-netmask': '255.255.0.0',
        'net-gateway': '10.0.0.254',
        'net-nameserver': '8.8.8.8,8.8.4.4',
        'root-password': 'geencryptrootwachtwoord',
        'user-name': 'admin',
        'user-gecos': 'Administrator',
        'user-groups': 'wheel,anderegroep',
        'user-password': 'geencryptuserpassword'
    }
    db.write_host(data2)
    data3 = {
        'id': str(uuid.uuid4()),
        'order': 4,
        'net-hostname': 'host3.test.lab',
        'net-type': 'static',
        'net-ip': '10.0.0.3',
        'net-netmask': '255.255.255.0',
        'net-gateway': '10.0.0.254',
        'net-nameserver': '8.8.8.8,8.8.4.4',
        'root-password': 'geencryptrootwachtwoord',
        'user-name': 'admin',
        'user-gecos': 'Administrator',
        'user-groups': 'wheel,anderegroep',
        'user-password': 'geencryptuserpassword'
    }
    db.write_host(data3)
    data4 = {
        'id': str(uuid.uuid4()),
        'order': 3,
        'net-hostname': 'host4.test.lab',
        'net-type': 'static',
        'net-ip': '10.0.0.4',
        'net-netmask': '255.255.255.0',
        'net-gateway': '10.0.0.254',
        'net-nameserver': '8.8.8.8,8.8.4.4',
        'root-password': 'geencryptrootwachtwoord',
        'user-name': 'admin',
        'user-gecos': 'Administrator',
        'user-groups': 'wheel,anderegroep',
        'user-password': 'geencryptuserpassword'
    }
    db.write_host(data4)
    print("========== All hosts:\n", db.read_all_hosts())
    for i in db.read_all_hosts():
        print("ID: {}, Order: {}".format(i['id'], i['order']))
    db.delete_host(data1['id'])
    print("========== Host {}:\n".format(data2['id']), db.read_host(data2['id']))

def print_edit():
    id = db.read_all_hosts()[0]['id']
    return pageGenerator.generate_edit(id)

def print_ks():
    id = db.read_all_hosts()[0]['id']
    return pageGenerator.generate_kickstart(id)

# Actually call the test.
test_write()
##print(pageGenerator.generate_index())
#print(print_edit())
#print(pageGenerator.generate_redirect('https://tweakers.net'))
#print(print_ks())
#print(pageGenerator.edit_base_kickstart())
