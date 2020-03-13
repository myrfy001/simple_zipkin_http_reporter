# coding:utf-8

import os
import sys
import time
import requests
import traceback


def run(file_to_monit, zipkin_addr):

    sess = requests.session()
    old_fstate = None
    fd = open(file_to_monit, 'r', encoding='utf-8')

    while 1:
        try:

            line = fd.readline()
            if not line:
                time.sleep(0.5)
                if os.fstat(fd.fileno()).st_ino != os.stat(file_to_monit).st_ino:
                    fd.close()
                    fd = open(file_to_monit)
                continue
            else:
                ret = sess.post(
                    zipkin_addr,
                    data=line.encode('utf-8'),
                    headers={'Content-Type': 'application/x-thrift'}
                )
        except KeyboardInterrupt:
            raise SystemExit
        except Exception as e:
            traceback.print_exc()
            time.sleep(1)


if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2])
