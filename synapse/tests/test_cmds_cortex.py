from __future__ import absolute_import,unicode_literals

from contextlib import contextmanager

import synapse.cortex as s_cortex
import synapse.daemon as s_daemon
import synapse.telepath as s_telepath
import synapse.cmds.cortex as s_cmds_cortex

from synapse.tests.common import *

class SynCmdCoreTest(SynTest):

    @contextmanager
    def getDmonCore(self):

        dmon = s_daemon.Daemon()
        core = s_cortex.openurl('ram:///')

        link = dmon.listen('tcp://127.0.0.1:0/')
        dmon.share('core00',core)
        port = link[1].get('port')
        prox = s_telepath.openurl('tcp://127.0.0.1/core00', port=port)

        s_scope.set('syn:test:link',link)
        #s_scope.set('syn:test:dmon',dmon)

        s_scope.set('syn:cmd:core',prox)

        yield prox

        prox.fini()
        core.fini()
        dmon.fini()

    def getCoreCmdr(self):
        outp = s_output.OutPutStr()
        return s_cmds_cortex.initCoreCli(outp=outp)

    def test_cmds_addnode(self):
        with self.getDmonCore() as core:
            cmdr = self.getCoreCmdr()
            cmdr.runCmdLine('addnode inet:email visi@vertex.link')
            self.nn( core.getTufoByProp('inet:email','visi@vertex.link') )

    def test_cmds_addtag(self):

        with self.getDmonCore() as core:
            cmdr = self.getCoreCmdr()

            core.formTufoByProp('inet:email','visi@vertex.link')

            cmdr.runCmdLine('addtag woot inet:email="visi@vertex.link"')

            node = core.formTufoByProp('inet:email','visi@vertex.link')
            self.nn( node[1].get('*|inet:email|woot') )

    def test_cmds_deltag(self):

        with self.getDmonCore() as core:
            cmdr = self.getCoreCmdr()

            node = core.formTufoByProp('inet:email','visi@vertex.link')
            core.addTufoTag(node,'woot')

            cmdr.runCmdLine('deltag woot inet:email="visi@vertex.link"')

            node = core.getTufoByProp('inet:email','visi@vertex.link')
            self.none( node[1].get('*|inet:email|woot') )

    def test_cmds_ask(self):
        # FIXME moar robust output testing
        with self.getDmonCore() as core:
            cmdr = self.getCoreCmdr()
            core.formTufoByProp('inet:email','visi@vertex.link')
            resp = cmdr.runCmdLine('ask inet:email="visi@vertex.link"')
            self.eq( len(resp['data']), 1 )
