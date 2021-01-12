# frozen_string_literal: true

require 'rubygems'
require 'net/http'
require 'uri'
require 'xmlsimple'

# require 'AuthBase'
load 'AuthBase.rb'

class WizIQClass
  def initialize; end

  def get_teacher_details(access_key, secret_key, serviceUrl,data_hash)
    oAuthBase = AuthBase.new

    requestParameters = {}
    requestParameters['access_key'] = access_key
    time = Time.now
    requestParameters['timestamp'] = oAuthBase.GenerateTimeStamp
    requestParameters['method'] = 'get_teacher_details'
    # puts oAuthBase.GenerateSignature(secret_key,requestParameters)

    requestParameters['signature'] = oAuthBase.GenerateSignature(secret_key, requestParameters)
    requestParameters['teacher_id'] = data_hash['teacher_id']
    return_xml = oAuthBase.WiZiQWebRequest(serviceUrl + '?method=get_teacher_details', requestParameters)
    return_xml
  end

  def add_teacher(access_key, secret_key, serviceUrl,data_hash)
    oAuthBase = AuthBase.new

    requestParameters = {}
    requestParameters['access_key'] = access_key
    time = Time.now
    requestParameters['timestamp'] = oAuthBase.GenerateTimeStamp
    requestParameters['method'] = 'add_teacher'
    # puts oAuthBase.GenerateSignature(secret_key,requestParameters)
    requestParameters['signature'] = oAuthBase.GenerateSignature(secret_key, requestParameters)
    requestParameters['name'] = data_hash['name']
    requestParameters['email'] = data_hash['email']
    requestParameters['password'] = data_hash['password']
    requestParameters['image'] = data_hash['image']
    requestParameters['phone_number'] = data_hash['phone_number']
    requestParameters['mobile_number'] = data_hash['mobile_number']
    requestParameters['time_zone'] = data_hash['time_zone']
    requestParameters['about_the_teacher'] = data_hash['about_the_teacher']
    requestParameters['can_schedule_class'] = data_hash['can_schedule_class']
    requestParameters['is_active'] = data_hash['is_active']
    return_xml = oAuthBase.WiZiQWebRequest(serviceUrl + '?method=add_teacher', requestParameters)
    return_xml
  end

  def Create(access_key, secret_key, serviceUrl,data_hash)
    oAuthBase = AuthBase.new

    requestParameters = {}
    requestParameters['access_key'] = access_key
    time = Time.now
    requestParameters['timestamp'] = oAuthBase.GenerateTimeStamp
    requestParameters['method'] = 'create'
    # puts oAuthBase.GenerateSignature(secret_key,requestParameters)

    requestParameters['signature'] = oAuthBase.GenerateSignature(secret_key, requestParameters)
    # This is the unique email of the presenter that will identify the presenter in WizIQ. Make sure to add
    # this presenter email to your organization�s teacher account.
    # For more information visit at: (http://developer.wiziq.com/faqs)
    requestParameters['presenter_email'] = data_hash['presenter_email']
    # for room based account pass presenter_id, presenter_name
    # requestParameters["presenter_id"] = "34"
    # requestParameters["presenter_name"] = "vinugeorge"
    requestParameters['start_time'] = Time.now
    requestParameters['title'] = data_hash['title']
    requestParameters['extend_duration'] = data_hash['extend_duration']
    requestParameters['duration'] = data_hash['duration']
    requestParameters['attendee_limit'] = data_hash['attendee_limit']
    requestParameters['return_url'] = data_hash['return_url']
    requestParameters['language_culture_name'] = data_hash['language_culture_name']
    requestParameters['presenter_default_controls'] = data_hash['presenter_default_controls']
    requestParameters['attendee_default_controls'] = data_hash['attendee_default_controls']
    requestParameters['create_recording'] = data_hash['create_recording']
    return_xml = oAuthBase.WiZiQWebRequest(serviceUrl + '?method=create', requestParameters)
    return_xml
    #  puts return_xml
    #  puts return_xml['status']
    #    if (return_xml['status']=='ok')
    #      then
    #      puts 'process return_xml'
    #    end
  end # end create

  def Modify(access_key, secret_key, serviceUrl)
    oAuthBase = AuthBase.new

    requestParameters = {}
    requestParameters['access_key'] = access_key
    requestParameters['timestamp'] = oAuthBase.GenerateTimeStamp
    requestParameters['method'] = 'modify'

    # puts oAuthBase.GenerateSignature(secret_key,requestParameters)

    requestParameters['signature'] = oAuthBase.GenerateSignature(secret_key, requestParameters)

    requestParameters['class_id'] = '5817'
    requestParameters['presenter_name'] = 'vinugeorge'
    # requestParameters["start_time"] = "2011-04-28 12:00"
    # requestParameters["title"]="my ruby class-ROR-2"

    return_xml = oAuthBase.WiZiQWebRequest(serviceUrl + '?method=modify', requestParameters)

    return_xml
    #    puts return_xml
    #    puts return_xml['status']
    #    if (return_xml['status']=='ok')
    #      then
    #      puts 'process return_xml'
    #    end
  end

  def AddAttendees(access_key, secret_key, serviceUrl,data_hash)
    oAuthBase = AuthBase.new

    requestParameters = {}
    requestParameters['access_key'] = access_key
    requestParameters['timestamp'] = oAuthBase.GenerateTimeStamp
    requestParameters['method'] = 'add_attendees'

    # puts oAuthBase.GenerateSignature(secret_key,requestParameters)

    requestParameters['signature'] = oAuthBase.GenerateSignature(secret_key, requestParameters)
    requestParameters['class_id'] = data_hash['class_id']
    requestParameters['attendee_list'] = data_hash['attendee_list']

    return_xml = oAuthBase.WiZiQWebRequest(serviceUrl + '?method=add_attendees', requestParameters)
    return_xml
    #    puts return_xml
    #    puts return_xml['status']
    #    if (return_xml['status']=='ok')
    #      then
    #      puts 'process return_xml'
    #    end
  end

  def Cancel(access_key, secret_key, serviceUrl,data_hash)
    oAuthBase = AuthBase.new

    requestParameters = {}
    requestParameters['access_key'] = access_key
    time = Time.now
    requestParameters['timestamp'] = oAuthBase.GenerateTimeStamp
    requestParameters['method'] = 'cancel'

    # puts oAuthBase.GenerateSignature(secret_key,requestParameters)

    requestParameters['signature'] = oAuthBase.GenerateSignature(secret_key, requestParameters)

    requestParameters['class_id'] = data_hash['class_id']

    return_xml = oAuthBase.WiZiQWebRequest(serviceUrl + '?method=cancel', requestParameters)
    return_xml
    #    puts return_xml
    #    puts return_xml['status']
    #    if (return_xml['status']=='ok')
    #      then
    #      puts 'process return_xml'
    #    end
  end

  def Download_recording(access_key, secret_key, serviceUrl,data_hash)
    oAuthBase = AuthBase.new

    requestParameters = {}
    requestParameters['access_key'] = access_key
    time = Time.now
    requestParameters['timestamp'] = oAuthBase.GenerateTimeStamp
    requestParameters['method'] = 'download_recording'

    # puts oAuthBase.GenerateSignature(secret_key,requestParameters)

    requestParameters['signature'] = oAuthBase.GenerateSignature(secret_key, requestParameters)

    requestParameters['class_id'] = data_hash['class_id']

    # recording_format value can be zip, exe or mp4
    # mp4 recording is available only for classes conducted on WizIQ desktop app
    requestParameters['recording_format'] = data_hash['recording_format']
    return_xml = oAuthBase.WiZiQWebRequest(serviceUrl + '?method=download_recording', requestParameters)
    return_xml
     #    puts return_xml
     #    puts return_xml['status']
     #    if (return_xml['status']=='ok')
     #      then
     #      puts 'process return_xml'
     #    end
   end
end
