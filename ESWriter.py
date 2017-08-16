# -*- coding: utf-8 -*-
__author__ = 'krasnoyarov_ai@comp-tech.ru'

import lxml.etree as etree
nsSpa1 = "urn://x-artefacts-rosreestr-ru/commons/complex-types/entity-spatial/1.0.2"
nsSpa2="urn://x-artefacts-rosreestr-ru/commons/complex-types/entity-spatial/2.0.1"

class Ordinate:
    def __init__(self,pnode):
        self.xmlName = "Ordinate"
        self.pnode = pnode
    def write(self,x,y,n,d,pp,gopr,gzac=""):
        self.xmlNode = etree.SubElement(self.pnode,"{"+nsSpa2+"}"+self.xmlName)
        self.xmlNode.set("X",x)
        self.xmlNode.set("Y",y)
        self.xmlNode.set("NumGeopoint",n)
        self.xmlNode.set("DeltaGeopoint",d)
        if pp:
            self.xmlNode.set("PointPref",pp)
        self.xmlNode.set("GeopointOpred",gopr)
        if gzac:
            self.xmlNode.set("GeopointZacrep",gzac)

class SpelementUnit:
    def __init__(self,pnode):
        self.xmlName = "SpelementUnit"
        self.pnode = pnode
    def write(self,tu,sn):
        self.xmlNode = etree.SubElement(self.pnode,"{"+nsSpa2+"}"+self.xmlName)

        self.xmlNode.set("TypeUnit",tu)
        if sn:
            self.xmlNode.set("SuNmb",sn)
        return Ordinate(self.xmlNode)

class SpatialElement:
    def __init__(self,pnode):
        self.xmlName = "SpatialElement"
        self.pnode = pnode
    def write(self):
        self.xmlNode = etree.SubElement(self.pnode,"{"+nsSpa2+"}"+self.xmlName)
        return SpelementUnit(self.xmlNode)