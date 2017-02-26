import sqlite3
#TODO Change path to /data before putting it in a Docker container.
DATABASE_PATH = '/tmp/ksdb.sqlite'

def createdb():
    """Create a new database."""
    sql = """CREATE TABLE hosts (
        "id" text PRIMARY KEY,
        "order" integer,
        "net-hostname"
        "net-hostname" text,
        "net-type" text,
        "net-ip" text,
        "net-netmask" text,
        "net-gateway" text,
        "net-nameserver" text,
        "root-password" text,
        "user-name" text,
        "user-gecos" text,
        "user-groups" text,
        "user-password" text);"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    conn.close()

def write_host(data):
    """Insert or update host entry. Function expects an dictionary with vars."""
    sql = """INSERT OR REPLACE INTO hosts (
        "id",
        "order",
        "net-hostname",
        "net-type",
        "net-ip",
        "net-netmask",
        "net-gateway",
        "net-nameserver",
        "root-password",
        "user-name",
        "user-gecos",
        "user-groups",
        "user-password"
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute(sql,
        [data['id'],
        data['order'],
        data['net-hostname'],
        data['net-type'],
        data['net-ip'],
        data['net-netmask'],
        data['net-gateway'],
        data['net-nameserver'],
        data['root-password'],
        data['user-name'],
        data['user-gecos'],
        data['user-groups'],
        data['user-password']])
    conn.commit()
    conn.close()

def delete_host(id):
    """Delete host with id."""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM hosts WHERE id = ?", [id,])
    conn.commit()
    conn.close()

def read_host(id):
    """Get all data of host with id."""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM hosts WHERE id = ?", [id,])
    data = c.fetchone()
    conn.close()
    return data

def read_all_hosts():
    """Get all data from the hosts table."""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM hosts")
    data = c.fetchall()
    conn.close()
    return data

def test_write():
    """Not to be used in production. Test code for this module."""
    import os
    os.remove(DATABASE_PATH)
    createdb()
    data1 = {
        'id': 'abc',
        'order': 1,
        'net-hostname': 'host1.test.lab',
        'net-type': 'dhcp',
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
    write_host(data1)
    data2 = {
        'id': 'def',
        'order': 2,
        'net-hostname': 'host2.test.lab',
        'net-type': 'dhcp',
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
    write_host(data2)
    print("========== All hosts:\n", read_all_hosts())
    delete_host('abc')
    print("========== Host def:\n", read_host('def'))
