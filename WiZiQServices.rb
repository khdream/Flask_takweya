# frozen_string_literal: true



require 'rubygems'

require 'net/http'

require 'uri'

require 'xmlsimple'

require 'json'

load 'WizIQClass.rb'

access_key = '7Q0Pdeveh24='

secret_key = 'ke92BAbYVAK3UyB+Rd8Axw=='

serviceUrl = 'http://classapi.wiziqxt.com/apimanager.ashx'

oWizIQClass = WizIQClass.new

# schedule a class

filename = ARGV[0]

file = File.read(filename)

data_hash = JSON.parse(file)

if data_hash['method'] == 'add_teacher'

  return_xml = oWizIQClass.get_teacher_details(access_key, secret_key, serviceUrl, data_hash)

  puts return_xml

  File.open(filename, 'w') do |f|

    f.write(return_xml.to_json)

  end

  if return_xml['status'] != 'ok' || data_hash['teacher_id'] == ''

    return_xml = oWizIQClass.add_teacher(access_key, secret_key, serviceUrl, data_hash)

    File.open(filename, 'w') do |f|

      f.write(return_xml.to_json)

    end
    puts return_xml
  end

end

if data_hash['method'] == 'create'

  return_xml = oWizIQClass.Create(access_key, secret_key, serviceUrl, data_hash)



  File.open(filename, 'w') do |f|

    f.write(return_xml.to_json)

  end



end



# modify a class



if data_hash['method'] == 'modify'



  return_xml = oWizIQClass.Modify(access_key, secret_key, serviceUrl)



  File.open(filename, 'w') do |f|

    f.write(return_xml.to_json)

  end



end



# #Add Attendees to a class



if data_hash['method'] == 'add_attendees'



  return_xml = oWizIQClass.AddAttendees(access_key, secret_key, serviceUrl, data_hash)



  File.open(filename, 'w') do |f|

    f.write(return_xml.to_json)

  end



end



# #Cancel a class



if data_hash['method'] == 'Cancel'



  return_xml = oWizIQClass.Cancel(access_key, secret_key, serviceUrl, data_hash)



  File.open(filename, 'w') do |f|

    f.write(return_xml.to_json)

  end



end



if data_hash['method'] == 'download'



  # Download_recording



  return_xml = oWizIQClass.Download_recording(access_key, secret_key, serviceUrl, data_hash)



  File.open(filename, 'w') do |f|

    f.write(return_xml.to_json)

  end



    # return_xml would be like



  end



# Download_recording



# return_xml=oWizIQClass.Download_recording(access_key,secret_key,serviceUrl)



# puts return_xml



# return_xml would be like



# <rsp status="ok">



# <method>download_recording</method>



# <download_recording status="true">



# <download_status>false</download_status>



# <message>Download Recording has been started..</message>



# <status_xml_path>http://wiziq.com/download/1234.xml</status_xml_path>



# </download_recording>



# </rsp>



# In the above download recording output xml there is a <status_xml_path>



# it would contain all the necessary status for the recording download



# sample xml



# <rsp status="ok"><method>download_recording</method><download_recording status="true"><download_status>true</download_status><message>ZIP Available</message>



# <recording_download_path>http://wiziq.com/recDownload/634510565359687500.zip</recording_download_path></download_recording>



# </rsp>

