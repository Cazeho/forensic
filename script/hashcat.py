""" A volatility Plugin for crack hashes """


import volatility.plugins.common as common 
import volatility.utils as utils
import volatility.win32 as win32
import volatility.win32.hashdump as hd
import volatility.plugins.registry.hivelist as hivelist
import volatility.plugins.registry.registryapi as registryapi
import volatility.cache as cache

# use remote wordlist : https://github.com/danielmiessler/SecLists/tree/master

def hash_decrypt():
   pass

class hashcat(common.AbstractWindowsCommand):
   """Crack NTLM hashes (need hashcat to run)"""
   
   def __init__(self, config, *args, **kwargs):
       common.AbstractWindowsCommand.__init__(self, config, *args, **kwargs)
       config.add_option('SYS-OFFSET', short_option='y', type='int', help="SYSTEM hive offset (virtual)")
       config.add_option('SAM-OFFSET', short_option="s", type='int', help='SAM hive offset (virtual)')
   


  # @cache.CacheDecorator(lambda self: "tests/hashdump/sys_offset={0}/sam_offset={1}".format(self._config.SYS_OFFSET, self._config.SAM_OFFSET))
   def calculate(self):
        addr=utils.load_as(self._config)

        if not self._config.sys_offset or not self._config.Sam_offset:
            regapi=registryapi.RegistryApi(self._config)
            for offset in regapi.all_offsets:
                name=regapi.all_offsets[offset].lower().split("\\")[-1]
                if "system" == name:
                   self._config.update("SYS_OFFSET",offset)
                elif "sam" == name:
                   self._config.update("SAM_OFFSET",offset)


        hashes=hd.dump_memory_hashes(addr,self._config,self._config.sys_offset,self._config.sam_offset)
        if hashes == None:
            debug.error("unable to read hashes from registry")
        return hashes
 
   def render_text(self, outfd, data):
        #outfd.write("{!s}\n".format(str(data)))
        for task in data:
               outfd.write("{!s}\n".format(str(task)))


"""
string = "Administrator:500:e52cac67419a9a224a3b108f3fa6cb6d:8846f7eaee8fb117ad06bdd830b7586c:::"
split_string = string.split(':')
filtered_list = list(filter(None, split_string))
print(filtered_list)
"""
