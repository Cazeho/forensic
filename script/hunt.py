""" A volatility Plugin for hunt IOCs in netscan """


import volatility.plugins.common as common 
import volatility.utils as utils
import volatility.win32 as win32
import volatility.win32.hashdump as hd
import volatility.plugins.registry.hivelist as hivelist
import volatility.plugins.registry.registryapi as registryapi


class hunt(common.AbstractWindowsCommand):
   """hunt IOCs in netcan"""
   
   
   def calculate(self):
        addr=utils.load_as(self._config)
        return addr
 
   def render_text(self, outfd, data):
        #outfd.write("{!s}\n".format(str(data)))
        for task in data:
               outfd.write("{!s}\n".format(str(task)))
