from BeautifulSoup import BeautifulSoup
import urllib2
import urlparse

def get_element(url, element, **kwargs):
    """Retrives elements and all its content from url.
    You can specifcy which element type 'div', 'a', 'p', ect in element.
    Then you can add any identifying features such as id="container" or class="box" in afterwards as **kwargs
    """
    try:
        html = BeautifulSoup(urllib2.urlopen(url).read()).find(element, **kwargs)
        print type(html)
        if not html:
            return False
        try:
            if "src" in html and url not in html:
                html['src'] = urlparse.urljoin(url,html['src'])
                print html
        except Exception as en:
            print en
            raise en
        return html
    except Exception as ex:
        print ex
        return False