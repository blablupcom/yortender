 # -*- coding: utf-8 -*-
import sys
reload(sys) # Reload does the trick!
sys.setdefaultencoding('UTF8')
from datetime import datetime
import urllib
#import BeautifulSoup
from bs4 import BeautifulSoup
from bs4 import NavigableString
import scraperwiki

def get_links_list (source_url):
    html = urllib.urlopen(source_url)
    soup = BeautifulSoup(html)
    links = soup.findAll('a', {'title':'View opportunity'})
    print links
    return links


def get_tender_soup (link):
    tender_url = base_url + link['href']
    tender_html = urllib.urlopen(tender_url)
    tender_soup = BeautifulSoup(tender_html)
    return tender_soup


def get_tender_id (tender_soup):

    if tender_soup.find('div',{"id":"formTitle"}) == None:
        print "+++++++++++++++  No tender ID - aborting (no formTitle div) ++++++++++++++++++++++++"
        exit()
    else:
        if tender_soup.find('div',{"id":"formTitle"}).findNext('h1') == None:
            print "+++++++++++++++  No tender ID - aborting (No H1 tag) ++++++++++++++++++++++++"
            exit()
        else:
            tender_id = tender_soup.find('div',{"id":"formTitle"}).findNext('h1').contents[0]
            if tender_id.startswith('Contract: '):
                tender_id = tender_id[len('Contract '):]

            print tender_id
            tender_id = tender_id.encode('utf-8')
            tender_id = tender_id.strip()
    return tender_id


def get_contents (tender_soup, tag, text, next_tag):
    if tender_soup.find(tag,text=text) == None:
        item_name = ''
        return item_name
    else:
        if len(tender_soup.find(tag,text=text).findNext(next_tag).contents) == 0:
            item_name = ''
            return item_name
        else:
            item_name = tender_soup.find(tag,text=text).findNext(next_tag).contents[0]
            item_name = item_name.encode('utf-8')
    return item_name


def get_estimates (tender_soup, tag, text, next_tag, alt_tag):
    if tender_soup.find(tag,text=text) == None:
        item_name = ''
        return item_name
    else:
        if len(tender_soup.find(tag,text=text).findNext(next_tag).contents) == 0:
            item_name = ''
            return item_name
        else:
            if len(tender_soup.find(tag,text=text).findNext(next_tag)) > 1:
                if len(tender_soup.find(tag,text=text).findNext(alt_tag).contents) == 0:
                    item_name = ''
                    return item_name
                else:
                    item_name = tender_soup.find(tag,text=text).findNext(alt_tag).contents[0]
            else:
                item_name = tender_soup.find(tag,text=text).findNext(next_tag).contents[0]

        item_name = item_name.encode('utf-8')
        item_name = item_name.strip()
    return item_name


def get_attr_text (tender_soup, tag, attr_type, attr_name): # where we use a tag's attributes to find previous tage and then use getText on next tag
    if tender_soup.find(tag,{attr_type : attr_name}) == None:
        print "+++++++++++++++  No address - aborting (No Address tag) ++++++++++++++++++++++++"
        exit()
    else:
        item_name = tender_soup.find(tag,{attr_type : attr_name}).getText()
        item_name = item_name.encode('utf-8')
    return item_name


def get_categories (tender_soup):
    span = tender_soup.find('div',{"id":"shCat_2"}).findNext('span')
    categories = [c.strip() for c in span.contents if isinstance(c, NavigableString)] # turn it into an array
    return categories


def get_text_text (tender_soup, tag, text, next_tag): # for use where we source the next tag by the text of the previous tag, but use getText() to extract the text
    if tender_soup.find(tag,text) == None:
        item_name = ''
    else:
        item_name = tender_soup.find(tag,text).findNext(next_tag)
        item_name = item_name.encode('utf-8')
    return


def get_address (tender_soup):
    if tender_soup.find('dt',text="Address:") == None:
        contact_addr = ''
    else:

        contact_addr = tender_soup.find('dt',text="Address:").findNext('dd') # get the dirty tag data (is stored in BS tag form)
        contact_addr = unicode(contact_addr) # turn it into a string
        contact_addr = contact_addr.split("<br") # split into an array

        for i in range(len(contact_addr)): # loop through the array
            contact_addr[i] = BeautifulSoup(contact_addr[i]).text # then use BeautifulSoup to extract the text and save it back into the array
            contact_addr[i] = contact_addr[i].replace(">","")
            contact_addr[i] = contact_addr[i].encode('utf-8')

    return str( contact_addr[0:len (contact_addr)-1 ] )
    #return str ( aList )



def get_attachments (tender_soup):
    attach_list = []
    if tender_soup.find("table", {"class":"altrows attachmentsTable"}) == None:
        pass
    else:
        rows = tender_soup.find("table", {"class":"altrows attachmentsTable"}).find("tbody").findAll("tr")
        for row in rows:
            att_name = row.findAll('td')[0].getText()
            att_size = row.findAll('td')[1].getText()
            att_date = row.findAll('td')[2].getText()
            att_url = row.findAll('td')[0].a['href']

            attach = [att_url,att_name,att_size,att_date]
            attach = [x.encode('utf-8') for x in attach]

            attach_list.append(attach)
    return attach_list


if __name__ == '__main__':

    todays_date = str(datetime.now())
    portals = [
    # 'https://www.londontenders.org/procontract/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    #'https://www.bluelight.gov.uk/procontract/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://www.fxplustenders.org/procontract/fxplus/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://www.lppsourcing.org/procontract/lpp/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://www.advantageswtenders.co.uk/procontract/advantage/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://www.bankofenglandtenders.co.uk/procontract/BankOfEngland/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://www.channelislandtenders.com/procontract/channelislands/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://www.eastmidstenders.org/procontract/emp/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://www.eastridingcontractsfinder.co.uk/procontract/eastriding/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://www.housingprocurement.com/procontract/housing/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://www.kentbusinessportal.org.uk/procontract/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://www.leedsth-tenders.co.uk/procontract/lth/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://tenders.metoffice.gov.uk/procontract/metoffice/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://www.qtegov.com/procontract/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://www.ncl-tenders.co.uk/procontract/newcastle/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://www.northumbriaunitenders.org/procontract/northumbria/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://www.supplying2nhs.com/procontract/healthservice/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://www.supplyingthesouthwest.org.uk/procontract/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://www.the-chest.org.uk/procontract/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://ukhocontracts.ukho.gov.uk/procontract/ukho/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://tender.bris.ac.uk/procontract/bristol/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
     'https://www.yortender.co.uk/procontract/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://www.ncl-tenders.co.uk/procontract/newcastle/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://www.sell2ea.com/procontract/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://ukhocontracts.ukho.gov.uk/procontract/ukho/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://www.dante-procurement.net/procontract/dante/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://tenders.lhc.gov.uk/procontract/lhc/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://www.wolverhamptontenders.com/procontract/wolverhampton/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://www.tenet4tenders.com/procontract/tenet/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://www.sanctuary-tenders.co.uk/procontract/sanctuary/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://www.standrewsprocurement.co.uk/procontract/standrews/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://www.geant-procurement.net/procontract/dante/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://www.ipoprocurement.co.uk/procontract/ipo/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL',
    # 'https://www.lgssprocurementportal.co.uk/procontract/NBC/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL'
    ]



    # saved_urls = df.values.tolist() # convert column to list
    # df = read_csv("dn16b.csv") # use pandas to open csv
    # saved_urls = df['tender_url'].values.tolist() # convert column to list
    #
    # resultFile = open("dn16b.csv",'a')


    for portal in portals:
        print portal
        base_url,temp = portal.split('/procontract/')
        links = get_links_list(portal)

        for link in links:

                linkcont = str(link.contents)
                linkstr = str(link)

            # if any(linkstr in s for s in saved_urls):
            #     print "got tender " + linkcont + " already."

                tender_soup = get_tender_soup(link); # grabs the html of a tender page and soups it.
                tender_id = get_tender_id(tender_soup); # gets the tender_id, no id? then we exit() in huff
                buyer = get_contents(tender_soup, "dt", "Buyer:", "dd");
                title = get_contents(tender_soup, "dt", "Title:", "dd");
                summary = get_attr_text(tender_soup,"dd","class","synopsis");
                categories = get_categories(tender_soup);

                contact_name = get_contents(tender_soup,"dt","Contact:","dd");
                contact_phone = get_contents(tender_soup, "dt","Telephone:","dd");

                #contact_email = get_text_text(tender_soup, "dt","Email Address:","dd");

                email_address = ""
                try:
                    contact_email = tender_soup.find("dt",text="Email Address:").findNext("dd").findNext("a").contents[0]
                except:
                    pass

                contact_addr = get_address(tender_soup);
                contract_start = get_contents(tender_soup,"label"," Estimated contract start date:","dd");
                contract_end = get_contents(tender_soup, "label"," Estimated contract end date:","dd");
                eoi_start = get_estimates(tender_soup, "label","Expression of interest start date:","dd","span");
                eoi_end = get_estimates(tender_soup, "label","Expression of interest end date:","dd","span");
                est_value = get_contents(tender_soup, "dt"," Estimated Value (£):","dd");
                contract_duration = get_contents(tender_soup, "label","Contract Period:","dd");
                extension_duration = get_contents(tender_soup, "label"," Anticipated Extension Period:","dd");
                extension_iterations = get_contents(tender_soup, "label","Number of Anticipated Extensions:","dd");

                attach_list = []
                attach_list = get_attachments(tender_soup)
                scraperwiki.sqlite.save(unique_keys=['l'], data={"l":unicode(link), "tender_id": unicode(tender_id), "buyer": unicode(buyer), "title" : unicode(title), "categories": unicode(categories), "contact_name": unicode(contact_name), "contact_phone": unicode(contact_phone), "contact_addr": unicode(contact_addr), "contact_email": unicode(contact_email), "contract_start": contract_start, "contract_end": contract_end, "eoi_start": eoi_start, "eoi_end": eoi_end, "est_value": unicode(est_value), "contract_duration": unicode(contract_duration), "extension_duration": unicode(extension_duration), "extension_iterations": unicode(extension_iterations), "summary": unicode(summary), "attach_list": unicode(attach_list),"d": todays_date })

                # csv_row = [link, tender_id,buyer,title,summary,categories,contact_name,contact_phone,contact_email,contact_addr,contract_start,contract_end,eoi_start,eoi_end,est_value,contract_duration,extension_duration,extension_iterations,attach_list]
                #
                # wr = csv.writer(resultFile, quoting=csv.QUOTE_ALL, delimiter=',')
                # wr.writerow(csv_row)



                # add other fields
                # add data to postgres
                # find a way to gather the data out of a google sheet




