#############################################################################
#                                                                           #
#                       Copyright 2020 Maria Nisar.                         #
#                           All Rights Reserved.                            #
#                                                                           #
# THIS WORK CONTAINS TRADE SECRET AND PROPRIETARY INFORMATION WHICH IS THE  #
#                   PROPERTY OF Maria Nisar                                 #
#                                                                           #
#############################################################################
'''
Module to Test Download Functionality.
@author: Maria Nisar
'''
import os
import urllib
import unittest
from download import Downloader


class DownloadTestCase(unittest.TestCase):
    def setUp(self):
        self.downloader = Downloader()

    def test_http_protocol(self):
        url = "https://github.com/CaliDog/certstream-python/archive/master.zip "
        file_name = url.split('/')[-1]
        size = 17347
        self.downloader.download_files(url)
        file_path = os.path.join(self.downloader.download_path, file_name)
        self.assertEqual(os.path.getsize(file_path), size)

    def test_ftp_protocol(self):
        url = "ftp://ftp.is.co.za/pub/squid/squid-3.1.23.tar.gz"
        file_name = url.split('/')[-1]
        size = 3489539
        self.downloader.download_files(url)
        file_path = os.path.join(self.downloader.download_path, file_name)
        self.assertEqual(os.path.getsize(file_path), size)

    def test_url_err(self):
        url = "ftp://mirror.aarnet.edu.au/pub/squid/archive/squid-4.0.15.tar.gz"
        with self.assertRaises(urllib.error.HTTPError):
            self.downloader.download(url)


if __name__ == "__main__":
    unittest.main()
