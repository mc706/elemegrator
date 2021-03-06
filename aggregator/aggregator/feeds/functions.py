from BeautifulSoup import BeautifulSoup
import urllib2

def get_element(url, element, **kwargs):
    """Retrives elements and all its content from url.
    You can specifcy which element type 'div', 'a', 'p', ect in element.
    Then you can add any identifying features such as id="container" or class="box" in afterwards as **kwargs
    """
    try:
        return BeautifulSoup(urllib2.urlopen(url).read()).find(element, **kwargs)
    except Exception as ex:
        print ex
        return False