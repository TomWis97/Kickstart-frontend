import os
import crypt
from . import db
from ipaddress import ip_network

basedir = os.path.dirname(os.path.abspath(__file__))
HTML_INDEX = open(os.path.join(basedir, 'index.html'), 'rt').read()
HTML_INDEX_BLOCK = open(os.path.join(basedir, 'index_block.html'), 'rt').read()
HTML_EDIT = open(os.path.join(basedir, 'edit.html'), 'rt').read()
HTML_EDIT_BASE = open(os.path.join(basedir, 'edit_base.html'), 'rt').read()
# TODO: Might want to change this path.
BASE_KICKSTART_LOCATION = os.path.join(basedir, '..', 'base.ks')
BASE_KICKSTART = open(BASE_KICKSTART_LOCATION).read()
KS_STATIC = ('network --bootproto=static --ip="{net_ip}"'
             '--netmask="{net_netmask}" --gateway="{net_gateway}"'
             '--nameserver="{net_nameserver}" --device=link')
KS_DHCP = 'network --bootproto=dhcp --device=link'
KS_ROOT = 'rootpw --iscrypted "{root_password}"'

# Note to self:
# For calculating subnetmasks, use ipaddress.ip_network.
# ip_network('0.0.0.0/255.255.255.0').prefixlen  -->  24
# str(ip_network('0.0.0.0/24').netmask)  -->  '255.255.255.0'

# Functions done:
# - generate_index
# - generate_edit
# - generate_redirect
# - generate_kickstart


def generate_index():
    """Generate index.html page."""
    allHosts = db.read_all_hosts()
    # Separate "done" hosts from "not done" hosts.
    notDoneHosts = []
    doneHosts = []
    for host in allHosts:
        if host['done'] == 0:
            notDoneHosts.append(host)
        elif host['done'] == 1:
            doneHosts.append(host)
        else:
            # "Done" should only be 0 (false) or 1 (true).
            raise ValueError
    notDoneHtml = ''
    for notDoneHost in notDoneHosts:
        notDoneHostHtml = HTML_INDEX_BLOCK.format(
            id=notDoneHost['id'],
            done='test',
            hostname=notDoneHost['net-hostname'],
            ip=notDoneHost['net-ip'])
        notDoneHtml = notDoneHtml + notDoneHostHtml
    doneHtml = ''
    for doneHost in doneHosts:
        doneHostHtml = HTML_INDEX_BLOCK.format(
            id=doneHost['id'],
            done='done',
            hostname=doneHost['net-hostname'],
            ip=doneHost['net-ip'])
        doneHtml = doneHtml + doneHostHtml
    return HTML_INDEX.format(remaining=notDoneHtml, done=doneHtml)


def generate_edit(id):
    """Generate the edit page for host with ID."""
    # This function demonstrates a nice part of the naming within this project:
    # some_variables_with_underscores, some_with_dashes_ and someWithCamelcase
    # Yes, I hate it too. But don't wanna change it at the risk of breaking.
    hostdata = db.read_host(id)
    # Regexes here, because str.format doesn't like curly brackets.
    regex_hostname = ('^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)'
                      '*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$')
    regex_ip = ('^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}'
                '([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$')
    net_netmask = ip_network('0.0.0.0/' + hostdata['net-netmask']).prefixlen
    # Extract the 3 DHCP servers.
    dnsList = hostdata['net-nameserver'].split(',')
    # This makes me feel dirty.
    try:
        net_dns_1 = dnsList[0]
    except:
        net_dns_1 = ''
    try:
        net_dns_2 = dnsList[1]
    except:
        net_dns_2 = ''
    try:
        net_dns_3 = dnsList[2]
    except:
        net_dns_3 = ''
    # Set net_type_dhcp or net_type_static to "checked", depending on net-type.
    if hostdata['net-type'] == 'dhcp':
        net_type_dhcp = 'checked'
        net_type_static = ''
    elif hostdata['net-type'] == 'static':
        net_type_dhcp = ''
        net_type_static = 'checked'
    else:
        raise ValueError('Invalid net-type for host id {}'.format(id))
    return HTML_EDIT.format(
        regex_ip=regex_ip,
        regex_hostname=regex_hostname,
        id=id,
        net_hostname=hostdata['net-hostname'],
        net_type_static=net_type_static,
        net_type_dhcp=net_type_dhcp,
        net_ip=hostdata['net-ip'],
        net_netmask=net_netmask,
        net_gateway=hostdata['net-gateway'],
        net_dns_1=net_dns_1,
        net_dns_2=net_dns_2,
        net_dns_3=net_dns_3,
        root_password=hostdata['root-password'],
        user_name=hostdata['user-name'],
        user_gecos=hostdata['user-gecos'],
        user_groups=hostdata['user-groups'],
        user_password=hostdata['user-password'])


def generate_kickstart(id):
    """Generate the kickstart file of the host with ID."""
    # TODO: What if host doesn't exist?
    data = db.read_host(id)
    # Special treatment items:
    # network settings: Line depends on dhcp or static.
    if data['net-type'] == 'dhcp':
        net_settings = KS_DHCP
    elif data['net-type'] == 'static':
        net_settings = KS_STATIC.format(
            net_ip=data['net-ip'],
            net_netmask=data['net-netmask'],
            net_gateway=data['net-gateway'],
            net_nameserver=data['net-nameserver'])
    else:
        net_settings = ''
    if data['root-password'] == '':
        root_settings = ''
    else:
        root_settings = KS_ROOT.format(root_password=data['root-password'])
    return BASE_KICKSTART.format(
        net_settings=net_settings,
        root_settings=root_settings,
        net_hostname=data['net-hostname'],
        user_name=data['user-name'],
        user_gecos=data['user-gecos'],
        user_groups=data['user-groups'],
        user_password=data['user-password'])


def generate_redirect(url):
    """Generate a redirect HTML page (with Javascript)."""
    baseHtml = """<!DOCTYPE html>
        <html>
            <head>
                <title>Redirect</title>
            </head>
            <body>
                <h1>Redirecting.</h1>
                <p>Redirecting you to <a href="{url}">{url}</a>.</p>
                <script>
                    alert("{url}");
                    window.location.replace("{url}");
                </script>
            </body>
        </html>"""
    return baseHtml.format(url=url)


def process_edit(data):
    """Process the POST data of a host edit. Expects dictionary with vars."""
    # Don't change password in database if it's still the hash.
    # If it's something else, it has to be hashed again.
    # Read current data.
    currentData = db.read_host(data['id'])
    if data['root-password'] != currentData['root-password']:
        data['root-password'] = crypt.crypt(data['root-password'])
    if data['user-password'] != currentData['user-password']:
        data['user-password'] = crypt.crypt(data['user-password'])
    # Check if order is integer.
    queueTop = False
    try:
        tmp = int(data['order'])
        if tmp == 0:
            queueTop = True
    except:
        queueTop = True
        data['order'] = 0
    # TODO: You shouldn't trust user input. Yet we just push everything to db.
    # WARNING: FIX THIS SECURITY HOLE.
    db.write_data(data)
    if queueTop:
        db.move_top(data['id'])
    return generate_redirect('index.html')


def process_move(id):
    """Move a host to the top of the queue."""
    db.move_top(id)
    return generate_redirect('index.html')


def process_delete(id):
    """Delete an host."""
    db.delete_host(id)
    return generate_redirect('index.html')


def open_first_kickstart():
    """Generate the first kickstart in the queue and mark it as "done"."""
    topId = db.get_top_id()
    db.mark_as_done(topId)
    return generate_kickstart(topId)


def edit_base_kickstart():
    """Generate HTML for editing base kickstart."""
    return HTML_EDIT_BASE.format(base_kickstart=BASE_KICKSTART)


def save_base_kickstart(base):
    # TODO: Finish this function.
    # Write new file to disk
    open(BASE_KICKSTART_LOCATION, 'wt').write(base)
    global BASE_KICKSTART
    BASE_KICKSTART = base
    return generate_redirect('index.html')
