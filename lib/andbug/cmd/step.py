#add by sq.luo
import andbug.command, andbug.screed
import andbug.vm

def stepComplete(t):
    t = t[0]
    with andbug.screed.section("Single step complete in %s, suspended." % t):
        showCallStack(t, 1)
        
def showCallStack(t, count = 0):
    if count >= len(t.frames) or count <= 0:
        count = len(t.frames)
    for f in t.frames[0:count]:
        name = str(f.loc)
        f.loc.method.firstLoc
        if f.native:
            name += ' <native>'
        andbug.screed.item(name)

def printValues(dist, name = None):
    if name == None:
        for key in dist.keys():
            print key + ' : ' + str(dist[key])
    else :
        if dist[name] != None:
            print name + ' : ' + str(dist[name]) 
            if (isinstance(dist[name], andbug.vm.Object)):
                print "{"
                printValues(dist[name].fields)
                print "}"
        else:
            print 'not found \"' + name + '\" variable'
            
@andbug.command.action('', aliases=('vs',))
def values(ctxt, name = None):
    'if you suspend, you print the values.'
    with andbug.screed.section('values'):
        if ctxt.sess.getSuspendState().isSuspend:
            t = ctxt.sess.getSuspendState().getThread()
            printValues(t.frames[0].values, name)
            
        else :
            print 'Not suspend, you can\'t print values'

@andbug.command.action('<variable name> <value>', aliases=('set', 'sv', ))
def setValues(ctxt, name = None, value = None):
    'if you suspend, you can set the values.'
    if name == None or value == None:
        print 'parameter not enough'
        return
    with andbug.screed.section('values'):
        if ctxt.sess.getSuspendState().isSuspend:
            t = ctxt.sess.getSuspendState().getThread()
            t.frames[0].setValue(name, value)
            
        else :
            print 'Not suspend, you can\'t print values'
                    
@andbug.command.action('[<count/all>]', aliases=('bt',))
def backtrace(ctxt, count = None):
    'if you suspend, you print the backtrace.'
    with andbug.screed.section('Back Trace'):
        if ctxt.sess.getSuspendState().isSuspend:
            t = ctxt.sess.getSuspendState().getThread()
            if count == 'all' or count == None:
                showCallStack(t)
            if count.isdigit():
                showCallStack(t, int(count))
            
        else :
            print 'Not suspend, you can\'t print backtrace'
                        
@andbug.command.action('', aliases=('s',))
def stepover(ctxt, expr=None):
    'if you suspend, you can step over.'
    with andbug.screed.section('Step Over'):
        if ctxt.sess.getSuspendState().isSuspend:
            t = ctxt.sess.getSuspendState().getThread()
            t.singleStep(func = stepComplete)
        else :
            print 'Not suspend, you can\'t step'
            
@andbug.command.action('', aliases=('si',))
def stepinto(ctxt, expr=None):
    'if you suspend, you can step into.'
    with andbug.screed.section('Step Into'):
        if ctxt.sess.getSuspendState().isSuspend:
            t = ctxt.sess.getSuspendState().getThread()
            t.singleStep(func = stepComplete, stepdepth = 0)
        else :
            print 'Not suspend, you can\'t step into'
            
@andbug.command.action('', aliases=('so',))
def stepout(ctxt, expr=None):
    'if you suspend, you can step out.'

    with andbug.screed.section('Step Out'):
        if ctxt.sess.getSuspendState().isSuspend:
            t = ctxt.sess.getSuspendState().getThread()
            t.singleStep(func = stepComplete, stepdepth = 2)
        else :
            print 'Not suspend, you can\'t step out'
