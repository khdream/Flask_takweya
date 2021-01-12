require 'hmac-sha1'
require 'base64'
require 'cgi'

class AuthBase
	
	def initialize
	end
    
	def GenerateTimeStamp
		time = Time.now
		return time.to_i
	end
	
	def GenerateSignature(private_key,requestParameters)
		   signatureBase=""
		   requestParameters.each  do|key, value|
			   #print key + ' = ' + value + "\n"
			  
			   if signatureBase.length>1 then
				   signatureBase+="&"
			   end	
			   signatureBase+="#{key}=#{value}"
			
		   end
		   #puts signatureBase
		  #signature
		  signature=Base64.encode64(HMAC::SHA1.digest(CGI::escape(private_key), signatureBase))
		  #puts signature.gsub!(/\n/, "")
		  return signature.gsub!(/\n/, "")
		  
	end	
	
	def WiZiQWebRequest(endpointUrl,requestParameters)
		  uri = URI.parse(endpointUrl)
		  
		  # POST 
		  http = Net::HTTP.new(uri.host, uri.port)
		  
		  
		  request = Net::HTTP::Post.new(uri.request_uri)
		  #request.set_form_data({"q" => "My query", "per_page" => "50"})
		  request.set_form_data(requestParameters)
		  response = http.request(request)
		  
		  #print response.body
		  
		  return_xml = XmlSimple.xml_in(response.body)
		  
		  return return_xml
	end	
end

