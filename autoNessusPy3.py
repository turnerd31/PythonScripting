import requests
import json
import sys
import argparse
import time
import datetime

# Disable Warning when not verifying SSL certs.
requests.packages.urllib3.disable_warnings()

# Create options and help menu
parser = argparse.ArgumentParser(description='Control Nessus with this script')
group = parser.add_mutually_exclusive_group()
group.add_argument('-l', '--list', dest='scan_list', action='store_true', help='List current scans and IDs')
group.add_argument('-p', '--policies', dest='policy_list', action='store_true', help='List current policies')
group.add_argument('-sS', '--start', dest='start_scan_id', type=str, help='Start a specified scan using scan id')
group.add_argument('-sR', '--resume', dest='resume_scan_id', type=str, help='Resume a specified scan using scan id')
group.add_argument('-pS', '--pause', dest='pause_scan_id', type=str, help='Pause a specified scan using scan id')
group.add_argument('-sP', '--stop', dest='stop_scan_id', type=str, help='Stop a specified scan using scan id')
group.add_argument('-cS', '--create', dest='create_scan_name', type=str, help='Create a scan using scan name')

args = parser.parse_args()
sname = "NoName"

if not len(sys.argv) > 1:
    parser.print_help()
    exit()

# Specify credentials for Nessus and initialize vars
url = 'https://YOURNESSUSURL:YOURPORT'
verify = False


class create_menu:
    '''This is used to build an instance of the menu object
       and can be called from the main program to instantiate the menu
       with passed variables.'''

    def __init__(self, menu, text, other):
        self.text = text
        self.menu = menu
        self.other = other

        # Build the menu
        option_length_menu = len(menu)
        option_length_text = len(text)
        if self.other != 'Null':
            print((
                '%s' + (20 - option_length_menu) * ' ' + '  :    %s' + (15 - option_length_text) * ' ' + ':    %s') % (
            menu, text, other))

        else:
            print(('%s' + (15 - option_length_menu) * ' ' + '  :  %s') % (menu, text))
        return


def build_url(resource):
    return '{0}{1}'.format(url, resource)


def connect(method, resource, data=None, params=None):
    """
    Send a request
    Send a request to Nessus based on the specified data. If the session token
    is available add it to the request. Specify the content type as JSON and
    convert the data to JSON format.
    """
    headers = {
        'X-ApiKeys': 'accessKey=APIKEY;''secretKey=SECRETKEY',
        'content-type': 'application/json'}

    data = json.dumps(data)

    if method == 'POST':
        print((build_url(resource), data, headers, verify))
        r = requests.post(build_url(resource), data=data, headers=headers, verify=verify)
    elif method == 'PUT':
        r = requests.put(build_url(resource), data=data, headers=headers, verify=verify)
    elif method == 'DELETE':
        r = requests.delete(build_url(resource), data=data, headers=headers, verify=verify)
    else:
        print((build_url(resource), params, headers, verify))
        r = requests.get(build_url(resource), params=params, headers=headers, verify=verify)

    # Exit if there is an error.
    if r.status_code != 200:
        e = r.json()
        print((e['error']))
        sys.exit()
        # When downloading a scan we need the raw contents not the JSON data.
    if 'download' in resource:
        return r.content

        # All other responses should be JSON data. Return raw content if they are
        # not.
    try:
        return r.json()
    except ValueError:
        return r.content


def get_policies():
    """
    Get scan policies
    Get all of the scan policies but return only the title and the uuid of
    each policy.
    """
    data = connect('GET', '/policies/')
    return dict((p['name'], p['template_uuid']) for p in data['policies'])


def get_scans():
    """
    Get history ids
    Create a dictionary of scans and uuids
    """

    status_dict = {}
    name_dict = {}
    data = connect('GET', '/scans/')
    for p in data['scans']:
        status_dict[p['id']] = p['status']
        name_dict[p['id']] = p['name']

    # status_dict = dict((p['name'], p['status']) for p in data['scans'])
    # id_dict = dict((b['name'], b['id']) for b in data['scans'])

    return status_dict, name_dict


def post_scans(sname,emails):
    """
	Create a scan with inputted scan name (scan name must be in target format)
	"""

    uuid = "ad629e16-03b6-8c1d-cef6-ef8c9dd3c658d24bd260ef5f9e66"
    enabled = "true"
    name = sname
    text_targets = sname
    
    data = {"uuid":uuid,"settings":{"name":name,"description":"Auto-Created with Nessus API","enabled":enabled,"emails": emails,"text_targets":text_targets,"rrules":"FREQ=MONTHLY;INTERVAL=1;","timezone":"US/Central","launch":"MONTHLY","starttime":time.strftime('%Y%m%dT%H%M%S')}}
    connect('POST', '/scans', data)
    return (data)


def get_history_ids(sid):
    """
    Get history ids
    Create a dictionary of scan uuids and history ids so we can lookup the
    history id by uuid.
    """
    data = connect('GET', '/scans/{0}'.format(sid))
    temp_hist_dict = dict((h['history_id'], h['status']) for h in data['history'])
    temp_hist_dict_rev = {a: b for b, a in list(temp_hist_dict.items())}
    try:
        for key, value in list(temp_hist_dict_rev.items()):
            print(key)
            print(value)
    except:
        pass
    # return dict((h['uuid'], h['history_id']) for h in data['history'])


def get_scan_history(sid, hid):
    """
    Scan history details
    Get the details of a particular run of a scan.
    """
    params = {'history_id': hid}
    data = connect('GET', '/scans/{0}'.format(sid), params)
    return data['info']


def get_status(sid):
    # Get the status of a scan by the sid.
    # Print out the scan status

    time.sleep(3)  # sleep to allow nessus to process the previous status change
    temp_status_dict, temp_name_dict = get_scans()
    print('\nScan Name           Status  ')
    print('---------------------------------------')
    for key, value in list(temp_name_dict.items()):
        if str(key) == str(sid):
            create_menu(value, temp_status_dict[key], 'Null')


def launch(sid):
    # Launch the scan specified by the sid.

    data = connect('POST', '/scans/{0}/launch'.format(sid))
    return data['scan_uuid']


def pause(sid):
    # Pause the scan specified by the sid.
    connect('POST', '/scans/{0}/pause'.format(sid))
    return


def resume(sid):
    # Resume the scan specified by the sid.
    connect('POST', '/scans/{0}/resume'.format(sid))
    return


def stop(sid):
    # Resume the scan specified by the sid.
    connect('POST', '/scans/{0}/stop'.format(sid))
    return


def logout():
    # Logout of Nessus.
    print('Logging Out...')
    connect('DELETE', '/session')
    print('Logged Out')
    exit()


if __name__ == '__main__':
    print(('Script started: ' + time.strftime('%m-%d-%y @ %H:%M:%S')))

    print('Logging in...')

    ###### Display all policies  #######
    if args.policy_list:
        # If -p flag is specified, print the policy list and exit

        print("Printing Policies \n\n")
        policy_dict = get_policies()
        print('Policy Name                              UUID')
        print('--------------------------------------------------')
        for name, template_uuid in list(policy_dict.items()):
            print((name, template_uuid))

    #######Create a scan #####
    if args.create_scan_name:
        # If -cS [scan_id] flag is passed, create the specified scan
        sname = args.create_scan_name
        emails = input("An email address is required for notication/ownership purposes. Please enter now: ")
        post_scans(sname,emails)
    ###### Display all scans  #######

    if args.scan_list:
        # If -l flag is specified, print the list of scans
        temp_status_dict, temp_name_dict = get_scans()
        print('Scan Name                  Status              ID')
        print('-------------------------------------------------')

        for status_id, status_value in list(temp_status_dict.items()):
            for name_id, name_value in list(temp_name_dict.items()):
                if status_id == name_id:
                    create_menu(name_value, status_value, status_id)

    # if args.start_scan_id:
    # If -sS [scan_id] flag is passed, start the specified scan
    #    start_id = args.start_scan_id
    #   temp_status_dict, temp_name_dict = get_scans()

    # Grab the status of the scan and either resume or start based on status
    #  for key, value in temp_name_dict.items():
    #     if str(key) == str(start_id):
    #        if temp_status_dict[key].lower() in ['stopped', 'completed', 'aborted', 'canceled', 'on demand', 'empty']:
    #          print('Launching Scan %s') % key
    #       launch(start_id)
    #     elif temp_status_dict[key].lower() in ['running']:
    #        print('Scan already running!')
    #   logout()
    #   else:
    #      print('Scan already started or paused.')
    #     print('If you need to start a previously completed scan, add "completed" to the list on line 269')
    #    logout()

    # Re-grab the scans to get the updated status
    # get_status(start_id)
    ###### Resume the scan  #######
    if args.resume_scan_id:
        # If -sR [scan_id] flag is passed, start the specified scan
        start_id = args.resume_scan_id
        temp_status_dict, temp_name_dict = get_scans()

        # Grab the status of the scan and either resume or start based on status
        for key, value in list(temp_name_dict.items()):
            if str(key) == str(start_id):
                if temp_status_dict[key].lower() in ['paused']:
                    print(('Resuming Scan %s') % key)
                    resume(start_id)
                elif temp_status_dict[key].lower() in ['running']:
                    print('Scan already running!')
                    logout()
                else:
                    print('Scan unable to start.')
                    print('If you need to start a previously completed scan, add "completed" to the list on line 269')
                    logout()

        get_status(start_id)

    ###### Pause the scan  #######
    elif args.pause_scan_id:
        # If -pS [scan_id] flag is passed, pause the specified scan
        pause_id = args.pause_scan_id
        temp_status_dict, temp_name_dict = get_scans()
        for key, value in list(temp_name_dict.items()):
            if str(key) == str(pause_id):
                if temp_status_dict[key].lower() in ['paused']:
                    print('Scan already paused!')
                    logout()
                elif temp_status_dict[key].lower() in ['running']:
                    print(('Pausing Scan %s') % key)
                    pause(pause_id)
                else:
                    print('Scan unable to be paused')
                    logout()

        # Re-grab the scans to get the updated status
        get_status(pause_id)

    ###### Stop the scan  #######
    elif args.stop_scan_id:
        # If -sP [scan_id] flag is passed, stop the specified scan

        stop_id = args.stop_scan_id
        temp_status_dict, temp_name_dict = get_scans()
        for key, value in list(temp_name_dict.items()):
            if str(key) == str(stop_id):
                if temp_status_dict[key].lower() in ['paused', 'running']:
                    print(('Stopping Scan %s') % key)
                    stop(stop_id)
                    logout()
                else:
                    print('Scan cannot be stopped!')
                    logout()

        # Re-grab the scans to get the updated status
        get_status(stop_id)
