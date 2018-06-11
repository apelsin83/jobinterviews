from io import BytesIO
import urllib
import urllib2
import re
import datetime
import pytesseract
from PIL import Image
import time


def error_decorator(func):
    """
    :param func: - function for wrapping
    :return: wrapped function
            decorator is responsible to repeat function
            after 1 second delay
    """
    def func_wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except:
                time.sleep(1)

    return func_wrapper


class Parser(object):

    def __init__(self):
        self.username = 'argos5652'
        self.password = 'ghgsl3lsf@'
        self.url = 'http://54.69.105.130/36e294b1d0dbe06a0cf626221ed54fc0'
        self.domain = 'http://54.69.105.130'
        self.pattern_captcha = re.compile(r'img.+?src="\.\.(.+?)".+?alt="CAPTCHA code"',
                                          re.IGNORECASE)
        self.pattern_cookie = re.compile(r'(.+?);.+')
        self.pattern_script = re.compile(r'<form\s+id=.ChallengeForm.\s+'
                                         r'action=.(.+?).\s+.+name=.(.+?)./>'
                                         r'.+?val\((.+?)\).+?submit.+?(\d+).+',
                                         re.IGNORECASE)
        self.pattern_links = re.compile(r'(<a.+?(index.php\?op=view&id=(\w+)'
                                        r'&.+?(?=[\"|\'])).+?\s.+?\s.+?Posted by'
                                        r'\s+(.+?),\s+(\d+)\s+seco.+?\s'
                                        r'.+?\s.+?\s.+?\s.*?</a>)',
                                        re.MULTILINE | re.IGNORECASE)
        self.pattern_text = re.compile(r'<p>(.*?cyberint\.com.*?)</p>',
                                       re.S | re.IGNORECASE)
        self.pattern_login_page = re.compile(r'<p\s+class=.section-paragraph.>\s*'
                                             r'Authentication\s+is\s+required\s+</p>',
                                             re.MULTILINE | re.IGNORECASE)
        self.headers = {'Connection': 'keep-alive',
                        'Cache-Control': 'max-age=0',
                        'Accept': 'text/html,application/xhtml+xml,'
                                  'application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Ubuntu Chromium/45.0.2454.101 '
                                      'Chrome/45.0.2454.101 Safari/537.36',
                        'Accept-Language': 'en-us,en;q=0.5'}

    def start_parsing(self):
        self.register_session()
        self.parse_page()

    @error_decorator
    def get_response(self, url, data=None):
        """
        :param url: url to get data from
        :param data: parameteres which need to pass to url

        :return: tuple with response object and html response
        """
        request = urllib2.Request(url, data, self.headers)
        response = urllib2.urlopen(request)
        return response, response.read()

    @error_decorator
    def register_session(self):
        """
        :return: function is responsible to get cookie session
                 and log in inside session
        """
        print 'Login....'
        if 'Cookie' in self.headers.keys():
            del self.headers['Cookie']
        response, html = self.get_response('%s/login.php' % self.url)
        if 'set-cookie' in response.headers.keys():
            self.headers['Cookie'], = self.find_value(self.pattern_cookie,
                                                      response.headers.get('Set-Cookie'), 1)
        image_url, = self.find_value(self.pattern_captcha, html, 1)
        captcha_url = '%s%s' % (self.domain, image_url)
        response, captcha = self.get_response(captcha_url)
        image_file = BytesIO(captcha)
        img = Image.open(image_file)
        code = pytesseract.image_to_string(img)
        code = filter(lambda x: x.isalnum(), code)
        post_data = {'input-username': self.username,
                     'input-password': self.password,
                     'input-captcha': code}
        response, html = self.get_response(
            '%s/login.php' % self.url, urllib.urlencode(post_data))
        url_dos, name, answer, timeout = self.find_value(
            self.pattern_script, html, 4)
        time.sleep(int(int(timeout) / 1000))
        post_data = {name: eval(answer)}
        self.get_response(
            '%s/%s' % (self.url, url_dos), urllib.urlencode(post_data))
        print 'Logged in ...'

    @staticmethod
    def find_value(pattern, text, number_groups):
        """
        :param pattern:
        :param text: text to parse
        :param number_groups: number of elements to return
        :return: tuple of found elements
        """
        m = re.search(pattern, text)
        return tuple([m.group(i) for i in range(1, number_groups + 1)])

    def get_article(self, link):
        """
        :param link: link of article
        :return: found text with cyberint.com or empty string
        """
        txt = ''
        response, html = self.get_response(link)
        match = re.search(self.pattern_text, html)
        if match:
            txt = match.group(1)
        return txt

    @staticmethod
    def get_post_time(now, delta):
        """
        :param now: datetime now
        :param delta: seconds ago when post was published
        :return: time of published post
        """
        post_time = now + datetime.timedelta(seconds=-int(delta))
        return post_time.strftime("%d/%m/%y %H:%M:%S")

    def parse_page(self):
        """
        :return: parsing in infinite loop posts
        """
        print 'Parsing.....'
        previous_article = ''
        self.headers['Referer'] = '%s/index.php'
        while True:
            try:
                response, html = self.get_response('%s/index.php' % self.url)
                links = re.findall(self.pattern_links, html)
                if links:
                    index = len(links)
                    dt_now = datetime.datetime.now()
                    for i in range(len(links)):
                        _, url, id_link, author, seconds = links[i]
                        if previous_article == id_link:
                            index = i
                            break
                    if index > 0:
                        _, url, id_link, author, seconds = links[index - 1]
                        previous_article = id_link
                        link = '%s/%s' % (self.url, url)
                        article_data = self.get_article(link)
                        if article_data:
                            print 'Author: %s\nLink: %s\nDate: %s\n%s\n%s' % \
                                  (author, link, self.get_post_time(dt_now, seconds),
                                   article_data, '-'*20)
                else:
                    # if session expired and need to relogin
                    login_page = re.findall(self.pattern_login_page, html)
                    if login_page:
                        self.register_session()
            except Exception as ex:
                print ex


if __name__ == "__main__":
    ob = Parser()
    ob.start_parsing()
