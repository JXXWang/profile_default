import sys,os,shutil,time
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        import pkg_resources
    except ImportError:
        pass
    else:
        del pkg_resources

if 'zmq' in sys.modules:
    # set 80 columns for non-terminal IPython
    # avoids super-wide ls/pager output in notebook
    os.environ['COLUMNS'] = '80'

ip = get_ipython()
for cls in ip.__class__.mro():
    if cls.__name__ == 'Application':
        app = cls.initialized() and cls.instance()

try:
    import zmq
except ImportError:
    print ('no zmq')
else:
    ctx = zmq.Context.instance()
    def create_bound_pair(type1=zmq.PAIR, type2=zmq.PAIR):
        sa = ctx.socket(type1)
        iface = 'tcp://127.0.0.1'
        p = sa.bind_to_random_port(iface)
        url = "%s:%i" % (iface, p)
        print (url)
        sb = ctx.socket(type2)
        sb.connect(url)
        for s in (sa, sb):
            if s.type == zmq.SUB:
                s.subscribe = b''
        return sa, sb

url = 'tcp://127.0.0.1:5555'
purl = 'tcp://127.0.0.1:%i'
localhost = 'tcp://127.0.0.1'

try:
    import numpy as np
except:
    pass