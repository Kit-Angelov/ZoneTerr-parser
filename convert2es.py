# -*- coding: utf-8 -*-
__author__ = 'Lord'

import csv
import io
from lxml import etree
import ESWriter as esw
import codecs

def csv2es(csvfile,ns,xmlsfile,xmldfile):
    csvf = codecs.open(csvfile,'r')
    #csvf = open(csvfile)
    d = csv.excel()
    d.delimiter = ';'
    csvr = csv.reader(csvf,d)

    csvr.next()
    xmlsf = open(xmlsfile)
    etree.register_namespace("spat2",esw.nsSpa2)
    root = etree.parse(xmlsf,base_url=ns)
    es = root.find(".//{"+ns+"}EntitySpatial")
    entsys = es.get("EntSys")
    es.clear()
    es.set("EntSys",entsys)


    spei = ''
    cn = 0

    for row in csvr:
        if row[0] == '':
            continue
        if spei != row[0]:
            spe = esw.SpatialElement(es)
            spuw = spe.write()
            spei = row[0]
            #cn = str(row[0]).strip('[,]')
            cn += 1
        spuw.write(u"Точка",str(cn)).write(row[5],row[6],row[2],u"5.0","",u"692003000000")

    xmldf = open(xmldfile,"w")
    xmldf.write(etree.tostring(root,pretty_print="true",encoding="utf-8"))
    csvf.close()
    xmlsf.close()
    xmldf.close()

def mif2es(miffile,ns,xmlsfile,xmldfile):
    miff = open(miffile,"r")
    xmlsf = open(xmlsfile)
    etree.register_namespace("spat2",esw.nsSpa2)
    root = etree.parse(xmlsf,base_url=ns)
    es = root.find(".//{"+ns+"}EntitySpatial")
    entsys = es.get("EntSys")
    es.clear()
    es.set("EntSys",entsys)

    line = miff.readline()

    nmb = 0
    cn =0
    while line:
        line = miff.readline()

        items = line.strip("\n").split(" ")
        #print items,len(items)
        if (len(items)==1) & (items[0].isdigit()):
            pcn = int(items[0])
            spe = esw.SpatialElement(es)
            cn = cn+1
            spuw = spe.write()
            #считываем перевую точку
            line = miff.readline()
            items = line.strip("\n").split(" ")
            sx = float(items[0])
            sy = float(items[1])
            #определяем счетчики точек
            nmb += 1
            pcn -= 1
            snmb=nmb
            #записываем первую точку
            spuw.write(u"Точка",str(nmb)).write(str(sy),str(sx),str(snmb),u"5.0","",u"692003000000")

            #считываем все точки контура кроме последней
            while pcn != 1:
                line = miff.readline()
                items = line.strip("\n").split(" ")
                x = float(items[0])
                y = float(items[1])
                nmb = nmb+1
                spuw.write(u"Точка",str(nmb)).write(str(y),str(x),str(nmb),u"5.0","",u"692003000000")
                pcn = pcn-1
            #записываем замыкающую точку
            nmb = nmb+1
            spuw.write(u"Точка",str(nmb)).write(str(sy),str(sx),str(snmb),u"5.0","",u"692003000000")
    # print cn
    xmldf = open(xmldfile,"w")
    xmldf.write(etree.tostring(root,pretty_print="true",encoding="utf-8"))
    miff.close()
    xmlsf.close()
    xmldf.close()

def mgisxy2esnode(mgisxyfile,es,d,gopr,delim=u"\t"):
    xyf = open(mgisxyfile,"r")

    entsys = es.get("EntSys")
    es.clear()
    es.set("EntSys",entsys)

    line = xyf.readline()

    nmb = 0

    while line:
        line = xyf.readline()

        items = line.strip("\n").split(delim)
        #определяем заговолок контура объекта (в т.ч. внутреннего)_
        if (items[0] == "xy")|((items[0] == "_")):
            #если раее осуществлялась запись точек в контур - добавляем замукающую
            if nmb != 0:
                nmb = nmb+1
                spuw.write(u"Точка",str(nmb)).write(str(sx),str(sy),str(snp),d,"",gopr)
            #создаем новый контур
            spe = esw.SpatialElement(es)
            #объект - запись координат
            spuw = spe.write()
            #считываем перевую точку
            line = xyf.readline()
            items = line.strip("\n").split(delim)
            sx = float(items[0])
            sy = float(items[1])
            snp = items[2]
            #определяем счетчики точек
            nmb = nmb+1
            #записываем первую точку
            spuw.write(u"Точка",str(nmb)).write(str(sx),str(sy),str(snp),d,"",gopr)
            continue

        if (len(items)==3):
            #if items[0].isdigit() & items[1].isdigit()& items[2].isdigit():
            items = line.strip("\n").split(delim)
            x = float(items[0])
            y = float(items[1])
            np = items[2]
            nmb = nmb+1
            spuw.write(u"Точка",str(nmb)).write(str(x),str(y),str(np),d,"",gopr)

    #замыкающая точка последнего контура
    #if spuw:
    nmb = nmb+1
    spuw.write(u"Точка",str(nmb)).write(str(sx),str(sy),str(snp),d,"",gopr)
    xyf.close()
