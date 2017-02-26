import sqlite3
#TODO Change path to /data before putting it in a Docker container.
DATABASE_PATH = '/tmp/ksdb.sqlite'
# Kickstart variables. The database also has columns for id and order.
VARIABLES = ('net-hostname', 'net-type', 'net-ip', 'net-netmask', 'net-gateway',
             'net-nameserver', 'root-password', 'user-name', 'user-gecos',
             'user-groups', 'user-password')

def createdb():
    """Create a new table with the given filename."""
    sql = """CREATE TABLE hosts (
        "id" text PRIMARY KEY,
        "order" integer,
        {}
    )"""
    # Some great code to dynamically generate the SQL query based on VARIABLES.
    varSql = ''
    for num, variable in enumerate(VARIABLES):
        varSql = varSql + '"' + variable + '"' + ' text'
        if not num == (len(VARIABLES)-1):
            # Don't add a ',' after the last variable.
            varSql = varSql + ', '
    sql = sql.format(varSql)
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    conn.close()

def write_host(data):
    """Insert or update host entry. Function expects an dictionary with vars."""
    if len(data) != (len(VARIABLES) + 2):
        raise ValueError("Too many or too few data items!")
    sql = """INSERT OR REPLACE INTO hosts (
        'id', 'order', {varList}) VALUES ("{id}", {order}, {varValues});"""
    # Again, some beautifully crafted code to generate the query. /s
    varList = ''
    for num, variable in enumerate(VARIABLES):
        varList = varList + '"' + variable + '"'
        # Don't insert an ',' after the last item.
        if not num == (len(VARIABLES)-1):
            varList = varList + ', '
    varValues = ''
    for num, variable in enumerate(VARIABLES):
        varValues = varValues + '"' + data[variable] + '"'
        # Don't insert an ',' after the last item.
        if not num == (len(VARIABLES)-1):
            varValues = varValues + ', '
    sql = sql.format(varList=varList, id=data['id'], order=data['order'],
                                                            varValues=varValues)
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    conn.close()

def test_write():
    createdb()
    data = {
        'id': 'abcd',
        'order': 123,
        'net-hostname': 'hostnaam',
        'net-type': 'dhcp',
        'net-ip': '127.0.0.1',
        'net-netmask': '255.255.255.0',
        'net-gateway': '127.0.0.2',
        'net-nameserver': '8.8.8.8,8.8.4.4',
        'root-password': 'geencryptrootwachtwoord',
        'user-name': 'admin',
        'user-gecos': 'Administrator',
        'user-groups': 'wheel,anderegroep',
        'user-password': 'geencryptuserpassword'
    }
    write_host(data)
