nano /usr/local/lib/python2.7/dist-packages/volatility/plugins/



apt install python2 python2.7-dev libpython2-dev -y
apt install python-pip
apt install subversion

pip2 install pycrypto
pip2 install distorm3

cd /usr/local/lib/python2.7/dist-packages/

svn export https://github.com/volatilityfoundation/volatility/trunk/volatility

mkdir -p /opt/volatility
cd /opt/volatility
EOF
chmod +x vol.py

ln -s $PWD/vol.py /usr/local/bin/volatility


#!/usr/bin/python2

import sys

if sys.version_info < (2, 6, 0):
    sys.stderr.write("Volatility requires python version 2.6, please upgrade your python installation.")
    sys.exit(1)

try:
    import psyco #pylint: disable-msg=W0611,F0401
except ImportError:
    pass

if False:
    # Include a fake import for things like pyinstaller to hit
    # since this is a dependency of the malware plugins
    import yara

import textwrap
import volatility.conf as conf
config = conf.ConfObject()
import volatility.constants as constants
import volatility.registry as registry
import volatility.exceptions as exceptions
import volatility.obj as obj
import volatility.debug as debug

import volatility.addrspace as addrspace
import volatility.commands as commands
import volatility.scan as scan

config.add_option("INFO", default = None, action = "store_true",
                  cache_invalidator = False,
                  help = "Print information about all registered objects")

def list_plugins():
    result = "\n\tSupported Plugin Commands:\n\n"
    cmds = registry.get_plugin_classes(commands.Command, lower = True)
    profs = registry.get_plugin_classes(obj.Profile)
    if config.PROFILE == None:
        config.update("PROFILE", "WinXPSP2x86")
    if config.PROFILE not in profs:
        raise BaseException("Invalid profile " + config.PROFILE + " selected")
    profile = profs[config.PROFILE]()
    wrongprofile = ""
    for cmdname in sorted(cmds):
        command = cmds[cmdname]
        helpline = command.help() or ''
        ## Just put the title line (First non empty line) in this
        ## abbreviated display
        for line in helpline.splitlines():
            if line:
                helpline = line
                break
        if command.is_valid_profile(profile):
            result += "\t\t{0:15}\t{1}\n".format(cmdname, helpline)
        else:
            wrongprofile += "\t\t{0:15}\t{1}\n".format(cmdname, helpline)

    if wrongprofile and config.VERBOSE:
        result += "\n\tPlugins requiring a different profile:\n\n"
        result += wrongprofile

    return result

def command_help(command):
    outputs = []
    for item in dir(command):
        if item.startswith("render_"):
            outputs.append(item.split("render_", 1)[-1])
    outputopts = "\nModule Output Options: " + \
        "{0}\n".format("{0}".format("\n".join([", ".join(o for o in sorted(outputs))]))) 

    result = textwrap.dedent("""
    ---------------------------------
    Module {0}
    ---------------------------------\n""".format(command.__class__.__name__))

    return outputopts + result + command.help() + "\n\n"

def print_info():
    """ Returns the results """
    categories = {addrspace.BaseAddressSpace: 'Address Spaces',
                  commands.Command : 'Plugins',
                  obj.Profile: 'Profiles',
                  scan.ScannerCheck: 'Scanner Checks'}
    for c, n in sorted(categories.items()):
        lower = (c == commands.Command)
        plugins = registry.get_plugin_classes(c, lower = lower)
        print "\n"
        print "{0}".format(n)
        print "-" * len(n)

        result = []
        max_length = 0
        for clsname, cls in sorted(plugins.items()):
            try:
                doc = cls.__doc__.strip().splitlines()[0]
            except AttributeError:
                doc = 'No docs'
            result.append((clsname, doc))
            max_length = max(len(clsname), max_length)

        for (name, doc) in result:
            print "{0:{2}} - {1:15}".format(name, doc, max_length)

def main():

    # Get the version information on every output from the beginning
    # Exceptionally useful for debugging/telling people what's going on
    sys.stderr.write("Volatility Foundation Volatility Framework {0}\n".format(constants.VERSION))
    sys.stderr.flush()

    # Setup the debugging format
    debug.setup()
    # Load up modules in case they set config options
    registry.PluginImporter()

    ## Register all register_options for the various classes
    registry.register_global_options(config, addrspace.BaseAddressSpace)
    registry.register_global_options(config, commands.Command)

    if config.INFO:
        print_info()
        sys.exit(0)

    ## Parse all the options now
    config.parse_options(False)
    # Reset the logging level now we know whether debug is set or not
    debug.setup(config.DEBUG)

    module = None
    ## Try to find the first thing that looks like a module name
    cmds = registry.get_plugin_classes(commands.Command, lower = True)
    for m in config.args:
        if m in cmds.keys():
            module = m
            break

    if not module:
        config.parse_options()
        debug.error("You must specify something to do (try -h)")

    try:
        if module in cmds.keys():
            command = cmds[module](config)

            ## Register the help cb from the command itself
            config.set_help_hook(obj.Curry(command_help, command))
            config.parse_options()

            if not config.LOCATION:
                debug.error("Please specify a location (-l) or filename (-f)")

            command.execute()
    except exceptions.VolatilityException, e:
        print e

if __name__ == "__main__":
    config.set_usage(usage = "Volatility - A memory forensics analysis platform.")
    config.add_help_hook(list_plugins)

    try:
        main()
    except Exception, ex:
        if config.DEBUG:
            debug.post_mortem()
        else:
            raise
    except KeyboardInterrupt:
        print "Interrupted"
