import datetime
from urllib.parse import urlencode, urlparse, quote
import urllib.parse
from urllib import request, parse
from base64 import b64encode
import base64
import hmac
import hashlib
from xml.etree import ElementTree as ET
import requests
import codecs
import re
from time import strftime, gmtime, strptime
class AuthBase:
    secretAcessKey=""
    access_key=""
    def __init__(self, secretAcessKey, access_key):
        self.secretAcessKey = secretAcessKey
        self.access_key = access_key
    def GenerateSignature(self, secretAcessKey, requestParameters):
        signatureBase = ""
        #requestParameters["access_key"] = self.access_key
        #requestParameters["timestamp"] = str(int(datetime.datetime.now().timestamp()))
        #requestParameters["method"] = methodName
        for key in requestParameters:
            if len(signatureBase) >0:
                signatureBase +='&'
            tempstr = key + '=' + requestParameters[key]
            signatureBase += tempstr
        print(signatureBase)
        key = urllib.parse.quote(secretAcessKey)
        key = bytes(key, 'UTF-8')
        message = bytes(signatureBase, 'UTF-8')
        digester = hmac.new(key, message, hashlib.sha1)
        signature1 = digester.digest()
        signature2 = base64.urlsafe_b64encode(signature1)
        return str(signature2, 'UTF-8')
        # signatureBase = signatureBase.encode('utf-8')
        # secretAcessKey1 = secretAcessKey.encode('utf-8')
        # hmac1 = hmac.new(secretAcessKey1, signatureBase, hashlib.sha1).hexdigest()
        # # hmac = HMAC.new(secretAcessKey,signatureBase,SHA1)
        # return str(b64encode(hmac1.encode("utf-8")), 'utf-8')
    def WiziQWebRequest(self, url, data):
        uri = urlparse(url)
        url1 = uri.scheme+"://" + uri.netloc+uri.path
        print(url1)
        postdata = parse.urlencode(data).encode()
        req = request.Request(url, data = postdata, method='POST')
        res = urllib.request.urlopen(req).read()
        return_xml = ET.fromstring(res.decode('utf-8'))
        #return_xml = ET.parse(res.read())
        #return return_xml.attrib
        return return_xml
    
    pass

class makeAPIClass:
    def createClass(self, secretAcessKey, access_key, webServiceUrl):
        authBase = AuthBase(secretAcessKey, access_key)
        method = "create"
        requestParameters = {}
        requestParameters["access_key"] = access_key
        requestParameters["timestamp"] = str(int(datetime.datetime.now().timestamp()))
        requestParameters["method"] = method
        requestParameters["signature"]=authBase.GenerateSignature(secretAcessKey,requestParameters)
        print(requestParameters["signature"])
        requestParameters['presenter_email'] = 'first@second.com'
        #requestParameters['presenter_email'] = create_one['mail']
        #requestParameters["presenter_id"] = "40";
        #requestParameters["presenter_name"] = "vinugeorge";  
        #requestParameters['start_time'] = datetime.datetime.now(datetime.).strftime("%Y-%m-%d %H:%M:%S.%f%Z")
        requestParameters['start_time'] = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
        print("--- time now ---")
        print(requestParameters['start_time'])
        
        requestParameters['title'] = 'ruby-class3'
        #requestParameters['title'] = create_one['title']
        requestParameters["duration"]="";
        requestParameters["time_zone"]="Asia/Kolkata";
        requestParameters["attendee_limit"]="";
        requestParameters["control_category_id"]="";
        requestParameters["create_recording"]="";
        requestParameters["return_url"]="";
        requestParameters["status_ping_url"]="";
        requestParameters["language_culture_name"]="en-us";
        return_xml = authBase.WiziQWebRequest(webServiceUrl + "?method=create", requestParameters)
        return return_xml
    def modifyClass(self, access_key,secretAcessKey,webServiceUrl):
        authBase = AuthBase(secretAcessKey, access_key)
        method = "modify"
        requestParameters = {} 
        requestParameters["access_key"] = access_key
        requestParameters["method"] = "modify"
        requestParameters["signature"]=authBase.GenerateSignature(method,requestParameters)
        requestParameters["class_id"] = "5817"
        requestParameters["presenter_name"] = "vinugeorge"  
        return_xml = authBase.WiziQWebRequest(webServiceUrl + "?method=modify", requestParameters)
        return return_xml
    def AddAttendees(self, access_key,secretAcessKey,webServiceUrl):
        authBase = AuthBase(secretAcessKey, access_key)
        method = "add_attendees"
        requestParameters = {} 
        requestParameters["access_key"] = access_key
        requestParameters["method"] = "add_attendees"
        requestParameters["signature"]=authBase.GenerateSignature(method,requestParameters)
        requestParameters["class_id"] = "5817"
        requestParameters["attendee_list"] = "<attendee_list><attendee><attendee_id><![CDATA[101]]></attendee_id><screen_name><![CDATA[john]]></screen_name></attendee><attendee><attendee_id><![CDATA[102]]></attendee_id><screen_name><![CDATA[mark]]></screen_name></attendee></attendee_list>"
        return_xml = authBase.WiziQWebRequest(webServiceUrl + "?method=add_attendees", requestParameters)
        return return_xml
    def CancelClass(self, access_key,secretAcessKey,webServiceUrl):
        authBase = AuthBase(secretAcessKey, access_key)
        method = "cancel"
        requestParameters = {} 
        requestParameters["access_key"] = access_key
        requestParameters["method"] = method
        requestParameters["signature"]=authBase.GenerateSignature(method,requestParameters)
        requestParameters["class_id"] = "5817"
        return_xml = authBase.WiziQWebRequest(webServiceUrl + "?method=cancel", requestParameters)
        return return_xml
    def Download_recording(self, access_key,secretAcessKey,webServiceUrl):
        authBase = AuthBase(secretAcessKey, access_key)
        method = "download_recording"
        requestParameters = {} 
        requestParameters["access_key"] = access_key
        requestParameters["method"] = method
        requestParameters["signature"]=authBase.GenerateSignature(method,requestParameters)
        requestParameters["class_id"] = "16833"
        requestParameters["recording_format"] = "zip"
        return_xml = authBase.WiziQWebRequest(webServiceUrl + "?method=download_recording", requestParameters)
        return return_xml
    def add_teacher(self, secretAcessKey, access_key, webServiceUrl):
        authBase = AuthBase(secretAcessKey, access_key)
        method = "add_teacher"
        requestParameters = {}
        requestParameters["access_key"] = access_key
        requestParameters["timestamp"] = str(int(datetime.datetime.now().timestamp()))
        print(requestParameters["timestamp"])
        requestParameters["method"] = method
        requestParameters["signature"]=authBase.GenerateSignature(method,requestParameters)
        print(requestParameters["signature"])
        requestParameters['name'] = 'Mike Lar'
        #requestParameters["presenter_id"] = "40";
        #requestParameters["presenter_name"] = "vinugeorge";  
        requestParameters['email'] = 'first@seacond.com'
        requestParameters['password'] = '123456'
        requestParameters["image"]=""
        requestParameters["phone_number"]="+1 1111111111"
        requestParameters["mobile_number"]="+1 1234567890"
        requestParameters["time_zone"]="Asia/Kolkata"
        requestParameters["about_the_teacher"]="Online Facilitator and Teacher, British Columbia, Canada";
        requestParameters["can_schedule_class"]=False
        requestParameters["is_active"]=True
        return_xml = authBase.WiziQWebRequest(webServiceUrl + "?method=add_teacher", requestParameters)
        return return_xml