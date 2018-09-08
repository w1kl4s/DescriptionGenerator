import os, sys
from Crypto.Hash import MD4
import time
import progressbar
import logging

def md4(x):
    h = MD4.new()
    h.update(x)
    return h

def generate_hash(filename, log):
    ed2k_block = 9500 * 1024
    ed2k_hash = b''
    file_size = None
    with open(filename, 'rb') as f:
        file_size = os.fstat(f.fileno()).st_size
        bar = 0
        currentblock = 0
        prefixes=('', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        if  type(log.handlers[0]) == logging.StreamHandler:
            widgets = [ progressbar.Percentage(), " | ",
                        progressbar.DataSize(prefixes = prefixes),"/",
                        progressbar.DataSize(variable="max_value", prefixes = prefixes), " | ",
                        progressbar.Bar(marker="#",left="[",right="]"),
                        progressbar.ETA()]
            progressbar.streams.wrap_stderr()
            bar = progressbar.ProgressBar(max_value=file_size, widgets = widgets)
        while True:
            block = f.read(ed2k_block)
            currentblock += sys.getsizeof(block)
            if not block:
                break
            ed2k_hash += md4(block).digest()

            if file_size % ed2k_block == 0:
                ed2k_hash += md4('').digest
            if bar:
                try:
                    bar.update(currentblock)
                except ValueError:
                    bar.finish()
                    #yes this is expected.
                    #sizes and bytes are black magic.
                    #maybe someday someone will have a better idea.
    ed2k_hash = md4(ed2k_hash).hexdigest()
    log.debug("Size: {}, hash: {}".format(file_size, ed2k_hash))
    return {"size": file_size, "hash": ed2k_hash}
