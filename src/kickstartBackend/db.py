import sqlite3
import uuid


# TODO Change path to /data before putting it in a Docker container.
DATABASE_PATH = '/tmp/ksdb.sqlite'


def _dict_factory(cursor, row):
    """Function required to create a dictionary instead of an tuple."""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def createdb():
    """Create a new database."""
    sql = """CREATE TABLE hosts (
        "id" text PRIMARY KEY,
        "order" integer,
        "done" integer,
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
    """Insert or update host entry. Expects an dictionary with vars."""
    if 'order' not in data:
        data['order'] = 0
    if 'done' not in data:
        data['done'] = 0
    sql = """INSERT OR REPLACE INTO hosts (
        "id",
        "order",
        "done",
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
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute(
        sql,
        [
            data['id'],
            data['order'],
            # Mark host as not done after submitting.
            0,
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
    c.execute('DELETE FROM hosts WHERE id = ?', [id, ])
    conn.commit()
    conn.close()


def read_host(id):
    """Get all data of host with id."""
    # TODO: Load defaults if host does not exist.
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = _dict_factory
    c = conn.cursor()
    c.execute('SELECT * FROM hosts WHERE id = ?', [id, ])
    data = c.fetchone()
    conn.close()
    return data


def read_all_hosts():
    """Get all data from the hosts table."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = _dict_factory
    c = conn.cursor()
    c.execute('SELECT * FROM hosts ORDER BY "order"')
    data = c.fetchall()
    conn.close()
    return data


def move_top(id):
    """Move host with ID to top by increasing the "order" value."""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('SELECT MAX("order") FROM hosts')
    maxOrder = c.fetchone()[0]
    newOrder = maxOrder + 1
    c.execute('UPDATE hosts SET "order" = ? WHERE id = ?', (newOrder, id))
    c.execute('UPDATE hosts SET "done" = 0 WHERE id = ?', (id, ))
    conn.commit()
    conn.close()
    return None


def get_top_id():
    """Get the id of the top host in the queue."""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('SELECT "id" FROM hosts WHERE "done" = 0 ORDER BY "order" DESC LIMIT 1')
    returnData = c.fetchone()
    if returnData == None:
        return 'default'
    else:
        return returnData[0]


def mark_as_done(id):
    if not id == 'default':
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute('UPDATE hosts SET "done" = 1 WHERE id = ?', (id, ))
        conn.commit()
        conn.close()
    return None
