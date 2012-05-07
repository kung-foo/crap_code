import os, sys, time
from pprint import pprint
import argparse
import httplib2
from urllib import urlencode

HIPCHAT_ROOM = 'MAG2-dev'

def main(args):
    if args.error.readline() != '':
        return

    cnt = 0

    f = ''
    
    for line in args.path:
        cnt += 1
        line = line.split("analyzer-ng")[1].strip()
        f += line + '\n'

    m = '<b>%s</b> commited %d file(s)<br />' % (args.user, cnt)
    m += 'Revision: %s<br />' % args.revision
    m += 'Log Message:<pre>%s</pre><br />' % args.messagefile.read().strip()
    m += 'Files:<br /><pre>%s</pre>' % f.strip()

    h = httplib2.Http()
    headers = {'Content-type': 'application/x-www-form-urlencoded'}

    p = {
        'room_id': HIPCHAT_ROOM,
        'color': 'purple',
        'from': 'svn-bot',
        'message': m
    }

    response, content = h.request('http://api.hipchat.com/v1/rooms/message?auth_token=%s' % args.auth_token, "POST", headers=headers, body=urlencode(p))

    return 0

if __name__ == '__main__':
    # PATH DEPTH MESSAGEFILE REVISION ERROR CWD 

    parser = argparse.ArgumentParser(description=sys.argv[0])

    parser.add_argument("--user")
    parser.add_argument("--auth-token")
    parser.add_argument("path", type=argparse.FileType('r'))
    parser.add_argument("depth")
    parser.add_argument("messagefile", type=argparse.FileType('r'))
    parser.add_argument("revision")
    parser.add_argument("error", type=argparse.FileType('r'))
    parser.add_argument("cwd")

    args = parser.parse_args()

    sys.exit(main(args))