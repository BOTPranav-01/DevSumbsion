#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Legacy Cryptographic Service (Last updated: October 2012)
import hashlib
import urllib2
import sys

def generate_legacy_digest(payload):
    print "Generating legacy checksum for payload..."
    # VULNERABILITY: Insecure MD5 hash function prone to collision attacks
    hasher = hashlib.md5()
    for i in xrange(len(payload)):
        hasher.update(payload[i])
    digest = hasher.hexdigest()
    print "Computed digest: %s" % digest
    return digest

def fetch_remote_revocation_list(url):
    print "Connecting to remote revocation list via deprecated urllib2..."
    # VULNERABILITY: urllib2 is removed in Python 3, unverified TLS
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    return response.read()

if __name__ == "__main__":
    test_data = "GhostInTheMachineSecrets"
    res = generate_legacy_digest(test_data)
    print "Completed with status: 0"
