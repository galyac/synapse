from synapse.tests.common import *

class CommonTest(SynTest):

    def test_common_vertup(self):
        self.eq(vertup('1.3.30'), (1, 3, 30))
        self.true(vertup('30.40.50') > (9, 0))

    def test_common_genfile(self):
        with self.getTestDir() as testdir:
            fd = genfile(testdir, 'woot', 'foo.bin')
            fd.close()

    def test_common_intify(self):
        self.eq(intify(20), 20)
        self.eq(intify("20"), 20)
        self.none(intify(None))
        self.none(intify("woot"))

    def test_common_guid(self):
        iden0 = guid()
        iden1 = guid('foo bar baz')
        iden2 = guid('foo bar baz')
        self.ne(iden0, iden1)
        self.eq(iden1, iden2)

    def test_common_isguid(self):
        self.true(isguid('98db59098e385f0bfdec8a6a0a6118b3'))
        self.false(isguid('visi'))

    def test_compat_canstor(self):
        self.true(0xf0f0)
        self.true(0xf0f0f0f0f0f0)
        self.true(canstor('asdf'))
        self.true(canstor(u'asdf'))
        # Ensure the previous two strings are actually the same string.
        self.eq(sys.intern('asdf'), sys.intern(u'asdf'))

        self.false(canstor(True))
        self.false(canstor(b'asdf'))
        self.false(canstor(('asdf',)))
        self.false(canstor(['asdf', ]))
        self.false(canstor({'asdf': True}))

    def test_common_listdir(self):
        with self.getTestDir() as dirn:
            path = os.path.join(dirn, 'woot.txt')
            with open(path, 'wb') as fd:
                fd.write(b'woot')

            os.makedirs(os.path.join(dirn, 'nest'))
            with open(os.path.join(dirn, 'nest', 'nope.txt'), 'wb') as fd:
                fd.write(b'nope')

            retn = tuple(listdir(dirn))
            self.len(2, retn)

            retn = tuple(listdir(dirn, glob='*.txt'))
            self.eq(retn, ((path,)))
