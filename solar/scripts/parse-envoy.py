import re
TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)
if True:
    import sys, BeautifulSoup
    html = BeautifulSoup.BeautifulSoup(open(sys.argv[1]).read())
    #print html
    #for td in html.findAll("td"):
    #    print "".join(td.contents) 
    info = html.findAll("td")
    current="".join(info[1].contents).strip('W')
    today="".join(info[3].contents).strip('Wh')
    systotal="".join(info[5].contents).strip('kWh')
    current = current.strip()
    today = today.strip()
    systotal = systotal.strip()
    systotal = float(systotal) * 1000
    print "OK|Solar_Current_Power=%s Solar_Today_Power=%s Solar_Sys_Total=%.1f" % (current,today,systotal)
