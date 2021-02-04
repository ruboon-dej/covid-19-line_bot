import requests

PROVINCES = ['Samut Sakhon', 'Bangkok', 'Chonburi', 'Samut Prakan', 'Rayong', 'Nonthaburi', 'Phuket', 'Chanthaburi', 'Songkhla', 'Yala', 'Pathum Thani', 'Nakhon Pathom', 'Pattani', 'Tak', 'Ang Thong', 'Chiang Rai', 'Chiang Mai', 'Narathiwat', 'Chachoengsao', 'Phra Nakhon Si Ayutthaya', 'Trat', 'Phetchaburi', 'Ratchaburi', 'Surat Thani', 'Nakhon Ratchasima', 'Krabi', 'Lopburi', 'Samut Songkhram', 'Chumphon', 'Satun', 'Prachuap Khiri Khan', 'Ubon Ratchathani', 'Prachinburi', 'Saraburi', 'Sing Buri', 'Unknown', 'Nakhon Si Thammarat', 'Buriram', 'Phatthalung', 'Kanchanaburi', 'Suphan Buri', 'Surin', 'Sa Kaeo', 'Nakhon Sawan', 'Khon Kaen', 'Loei', 'Udon Thani', 'Chaiyaphum', 'Phichit', 'Trang', 'Sisaket', 'Chainat', 'Phitsanulok', 'Lampang', 'Lamphun', 'Uttaradit', 'Nong Khai', 'Mae Hong Son', 'Nakhon Nayok', 'Phetchabun', 'Mukdahan', 'Sukhothai', 'Amnat Charoen', 'Phayao', 'Roi Et', 'Nong Bua Lamphu', 'Kalasin', 'Maha Sarakham', 'Kamphaeng Phet', 'Nakhon Phanom', 'Phang Nga', 'Yasothon', 'Phrae', 'Ranong', 'Uthai Thani', 'Nan', 'Sakon Nakhon']
PAGE_SIZE = 10

def get_provinces(index, page_size):
    start = index * page_size
    end = (index + 1) * page_size
    return PROVINCES[start:end]

def get_case_for_province(province):
    x = requests.get('https://covid19.th-stat.com/api/open/cases/sum')
    return x.json()['Province'][province]


def get_top_10(limit=10):
    x = requests.get('https://covid19.th-stat.com/api/open/cases/sum')
    provinces = x.json()['Province']
    sorted_provinces = sorted(provinces.items(), key=lambda item: -item[1])[:limit]

    ret = ""
    index = 0
    for (province, value) in sorted_provinces:
        index += 1
        end = "cases"
        ret += "{}. {}: {} {}\n".format(index, province, value, end)
    return ret[:-1] 