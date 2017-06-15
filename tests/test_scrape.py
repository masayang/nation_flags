import unittest
import mock
from nation_flags.scrape import (
    config, get_english_content, get_japanese_content, get_dom_tree, get_english_dom_tree,
    get_japanese_dom_tree, get_nation_name, get_flag_url, get_flag, get_nation_name_j,
    get_wikipedia_url, get_wikipedia_url_j, get_nations
)
from time import sleep
import urllib2

class TestScrape(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch('nation_flags.scrape.requests')
    def test_get_english_content(self, requests):
        requests.get.return_value = "content"
        with mock.patch.dict(config, {
            'ENGLISH_URL': "http://english_url.com/"
        }, clear=True):
            self.assertEquals(get_english_content(), "content")
            requests.get.assert_called_with('http://english_url.com/')

    @mock.patch('nation_flags.scrape.requests')
    def test_get_japanese_content(self, requests):
        requests.get.return_value = "content"
        with mock.patch.dict(config, {
            'JAPANESE_URL': "http://japanese_url.com/"
        }, clear=True):
            self.assertEquals(get_japanese_content(), "content")
            requests.get.assert_called_with('http://japanese_url.com/')

    @mock.patch('nation_flags.scrape.html')
    def test_get_dom_tree(self, html):
        html.fromstring.return_value = "dom_tree"
        self.assertEquals(get_dom_tree("content"), "dom_tree")
        html.fromstring.assert_called_with("content")

    @mock.patch('nation_flags.scrape.get_dom_tree')
    @mock.patch('nation_flags.scrape.get_english_content')
    def test_get_english_dom_tree(self, get_english_content, get_dom_tree):
        r = mock.MagicMock()
        r.content = "content"
        get_english_content.return_value = r
        get_dom_tree.return_value = "dom_tree"
        self.assertEqual(get_english_dom_tree(), "dom_tree")
        get_dom_tree.assert_called_with('content')
        get_english_content.assert_called_with()

    @mock.patch('nation_flags.scrape.get_dom_tree')
    @mock.patch('nation_flags.scrape.get_japanese_content')
    def test_get_japanese_dom_tree(self, get_japanese_content, get_dom_tree):
        r = mock.MagicMock()
        r.content = "content"
        get_japanese_content.return_value = r
        get_dom_tree.return_value = "dom_tree"
        self.assertEqual(get_japanese_dom_tree(), "dom_tree")
        get_dom_tree.assert_called_with('content')
        get_japanese_content.assert_called_with()

    def test_get_nation_name_Afghanistan(self):
        img_src = mock.MagicMock()
        img_src.attrib = {
            'alt': "Flag of  Afghanistan"
        }
        self.assertEquals(get_nation_name(img_src), "Afghanistan")

    def test_get_nation_name_Bahama(self):
        img_src = mock.MagicMock()
        img_src.attrib = {
            'alt': "Flag of the Bahamas"
        }
        self.assertEquals(get_nation_name(img_src), 'the Bahamas')

    def test_get_flag_url(self):
        img_src = mock.MagicMock()
        img_src.attrib = {
            'src': "image source"
        }
        self.assertEqual(get_flag_url(img_src), "image source")

    def test_get_flag_Japan(self):
        self.assertEqual(
            get_flag('//upload.wikimedia.org/wikipedia/en/thumb/9/9e/Flag_of_Japan.svg/150px-Flag_of_Japan.svg.png'),
            'Flag_of_Japan.svg')

    def test_get_flag_Australia(self):
        self.assertEqual(
            get_flag("//upload.wikimedia.org/wikipedia/commons/thumb/8/88/Flag_of_Australia_%28converted%29.svg/200px-Flag_of_Australia_%28converted%29.svg.png"),
            'Flag_of_Australia.svg')

    def test_get_flag_Belgium(self):
        self.assertEqual(
            get_flag(
                "//upload.wikimedia.org/wikipedia/commons/thumb/9/92/Flag_of_Belgium_%28civil%29.svg/150px-Flag_of_Belgium_%28civil%29.svg.png"),
            'Flag_of_Belgium.svg')

    def test_get_flag_Bolivia(self):
        self.assertEqual(
            get_flag(
                "//upload.wikimedia.org/wikipedia/commons/thumb/d/de/Flag_of_Bolivia_%28state%29.svg/147px-Flag_of_Bolivia_%28state%29.svg.png"),
            'Flag_of_Bolivia.svg')


    def test_get_flag_Switzerland(self):
        self.assertEqual(
        get_flag(
            "//upload.wikimedia.org/wikipedia/commons/thumb/0/08/Flag_of_Switzerland_%28Pantone%29.svg/100px-Flag_of_Switzerland_%28Pantone%29.svg.png"),
        'Flag_of_Switzerland.svg')

    def test_get_flag_Transnistria(self):
        self.assertEqual(
           get_flag(
                "//upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Flag_of_Transnistria_%28state%29.svg/200px-Flag_of_Transnistria_%28state%29.svg.png"),
            'Flag_of_Transnistria_%28state%29.svg')

    def test_get_nation_name_j(self):
        j_tree = mock.MagicMock()
        r = mock.MagicMock()
        r.attrib = {'alt': 'unicode'}
        j_tree.xpath.return_value = [r]
        self.assertEqual(get_nation_name_j(j_tree, "Japan"), "unico")
        j_tree.xpath.assert_called_with('//img[contains(@src, "Japan")]')

    def test_get_wikipedia_url_Japan(self):
        with mock.patch.dict(config, {
            'WIKIPEDIA_BASE_URL': "http://wikipedia/"
        }, clear=True):
            self.assertEquals(get_wikipedia_url("Japan"), "http://wikipedia/Japan")

    def test_get_wikipedia_url_j(self):
        with mock.patch.dict(config, {
            'WIKIPEDIA_BASE_URL_J': "http://ja.wikipedia/"
        }, clear=True):
            self.assertEquals(get_wikipedia_url_j("Japan".encode('utf-8')), "http://ja.wikipedia/Japan")

    def test_get_nations(self):
        nations =  get_nations()
        for nation in nations:
            self.assertEquals(urllib2.urlopen(nation['png_url']).getcode(), 200)
            sleep(1)
            self.assertEquals(urllib2.urlopen(nation['wikipedia_url_e']).getcode(), 200)
            sleep(1)
            self.assertEquals(urllib2.urlopen(nation['wikipedia_url_j']).getcode(), 200)
            sleep(1)