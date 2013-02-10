import urllib2
import bs4
import codecs
import re

# Dictionary of 'name':style color for use in naming files and identifying text
STYLE_DICT = {'gamzee': "color: #2b0057", 'dave':"color: #e00707",
              'john':"color: #0715cd", 'rose':"color: #b536da",
              'jade':"color: #4ac925", 'aradia':"color: #a10000",
              'tavros':"color: #a15000", 'sollux':"color: #a1a100",
              'karkat':"color: #626262", 'nepeta':"color: #416600",
              'kanaya':"color: #008141", 'terezi':"color: #008282",
              'vriska':"color: #005682", 'equius':"color: #000056",
              'eridan':"color: #6a006a", 'feferi':"color: #77003c",
              'jane':"color: #00d5f2", 'jake':"color: #1f9400",
              'dirk': "color: #f2a400", 'roxy':"color: #ff6ff2",
              'jaspersprite': "color: #f141ef", 'felt':"color: #2ed73a",
              'scratch':"color: #ffffff", 'calliope': "color: #929292",
              'caliborn': "color: #323232", "karkat_blood": "color: #ff0000"}

# How would I get only the chatlog on each page?
def is_chatbox(tag):
    if (tag.has_key('style') and
        tag['style'] == " font-weight: bold; font-family: courier, monospace;color:#000000" and
        tag.contents != [u'\n']):
        return True
    return False

def is_char_color(tag):
    if tag in STYLE_DICT.values():
        return True
    return False

#001901 - 007743
def scrape_homestuck():
    # first, open each page
    for i in range(7722, 7743, 2):
        url = 'http://www.mspaintadventures.com/?s=6&p=00' + str(i) + '\n'
        page = bs4.BeautifulSoup(urllib2.urlopen(url).read())
        # write texts to file
        f = codecs.open('homestuck_text.txt', mode = 'a', encoding = 'utf-8')
        chat_text = page.find_all(name = "span", style = is_char_color)
        # if there isn't character text, don't bother checking for characters
        if not chat_text:
            continue
        f.write(url) # keep track of pages
        for line in chat_text:
            print line.get_text()
            f.write(line.get_text())
            f.write('\n')
        # then check if each character talks on page

# some problems: for the double pages, some text was scraped twice.
def scrape_homestuck_characters():
    for i in range(7687, 7743, 2):
        url = 'http://www.mspaintadventures.com/?s=6&p=00' + str(i) + '\n'
        page = bs4.BeautifulSoup(urllib2.urlopen(url).read())
        # for each character, check if they are on the page, and if so,
        # append to .txt file
        for char in STYLE_DICT.keys():
            char_text = page.find_all(name = "span", style = STYLE_DICT[char])
            if not char_text:
                continue
            f = codecs.open(char + '.txt', mode = 'a', encoding = 'utf-8')
            f.write(url)
            for line in char_text:
                f.write(line.get_text())
                f.write('\n')

def create_training_data(file_name, num_lines):
    '''
    Creates a file called file_name + '_training.txt' from filename.
    num_lines is the number of lines that will be in training data.
    Strips out the url and any lines that contain [].
    '''
    source = open(file_name, 'r')
    dest_name = file_name.split('.')[0] + '_training.txt'
    print dest_name
    dest = open(dest_name, 'w')
    to_discard = re.compile(r'(\[..\])|http:')
    num_read = 0
    while num_read < num_lines:
        line = source.readline()
        if to_discard.search(line):
            continue
        print line
        dest.write(line)
        num_read += 1
    source.close()
    dest.close()

to_search = ['gamzee.txt', 'karkat.txt', 'eridan.txt', 'nepeta.txt',
             'equius.txt', 'feferi.txt', 'aradia.txt', 'john.txt', 'dave.txt',
             'sollux.txt', 'terezi.txt', 'rose.txt', 'kanaya.txt', 'tavros.txt',
             'vriska.txt', 'jade.txt']

for f in to_search:
    create_training_data(f, 200)
    
