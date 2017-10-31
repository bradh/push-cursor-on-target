import time as t
import uuid
import xml.etree.ElementTree as ET
import socket

ID = {
    "pending": "p",
    "unknown": "u",
    "assumed-friend": "a",
    "friend": "f",
    "neutral": "n",
    "suspect": "s",
    "hostile": "h",
    "joker": "j",
    "faker": "f",
    "none": "o",
    "other": "x"
}
DIM = {
    "space": "P",
    "air": "A",
    "land-unit": "G",
    "land-equipment": "G",
    "land-installation": "G",
    "sea-surface": "S",
    "sea-subsurface": "U",
    "subsurface": "U",
    "other": "X"
}

###################################################
def atoms_xml(unit):
    zulu = t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime())
    unit_id = ID[unit["identity"]] or ID["none"]
    
    cot_type = "a-" + unit_id + "-" + DIM[unit["dimension"]]
    if (len(unit["type"]) > 0):
        cot_type = cot_type + "-" + unit["type"]
    cot_id = uuid.uuid4().get_hex()
    
    evt_attr = {
        "version": "2.0",
        "uid": cot_id,
        "time": zulu,
        "start": zulu,
        "stale": zulu,
        "type": cot_type
    }

    pt_attr = {
        "lat": str(unit["lat"]),
        "lon":  str(unit["lon"]),
        "hae": "10",   #unit["hae"],
        "ce": "50",    #unit["ce"],
        "le": "50"     #unit["le"]1
    }
    
    cot = ET.Element('event', attrib=evt_attr)
    ET.SubElement(cot, 'detail')
    ET.SubElement(cot,'point', attrib=pt_attr)
    
    cot_xml = "<?xml version='1.0' standalone='yes'?'>" + ET.tostring(cot)
    return cot_xml

###################################################
def push_to_atak(ip_addr, port, cot_xml):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sent = sock.sendto(cot_xml, (ip_addr, port))
    print str(sent) + " bytes sent to " + ip_addr + ":" + str(port)
    return