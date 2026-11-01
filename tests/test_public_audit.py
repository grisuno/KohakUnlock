"""Publication matcher regression tests; addresses assembled from octets."""
import re
import unittest
from tools.audit_public import PATTERNS


class PublicAuditTests(unittest.TestCase):
    def test_section_numbers_are_not_addresses(self):
        for text in ('section 1.10.4.1.1 of FF-A', 'section 10.4.1.1.2'):
            self.assertIsNone(re.search(PATTERNS['private IPv4'], text))

    def test_private_addresses_still_detected(self):
        for octets in ((10, 1, 2, 3), (192, 168, 1, 2),
                       (172, 16, 1, 2), (172, 31, 1, 2)):
            address = '.'.join(map(str, octets))
            for text in (address, 'ssh user@' + address,
                         'https://' + address + ':443/', '(' + address + ')',
                         'host ' + address + '.'):
                self.assertIsNotNone(re.search(PATTERNS['private IPv4'], text))


if __name__ == '__main__':
    unittest.main()
