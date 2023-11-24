require './signer.rb'
require 'net/http'
require 'uri'

if __FILE__ == $PROGRAM_NAME
  sig = Signer.new
  sig.key = "apigateway_sdk_demo_key"
  sig.secret = "apigateway_sdk_demo_secret"

  r = HttpRequest.new("GET", "https://api-fake.dns.qihoo.net/apis/bifrost/ping?sn=12")
  r.headers = {"content-type" => "application/json"}
  r.body = ''
  sig.sign(r)
  puts r.headers["X-Sdk-Date"]
  puts r.headers["Authorization"]

  uri = URI.parse("#{r.scheme}://#{r.host}#{r.uri}")
  http = Net::HTTP.new(uri.host, uri.port)
  http.use_ssl = true if uri.scheme == 'https'
  request = Net::HTTP::Get.new(uri)
  request.initialize_http_header(r.headers)
  response = http.request(request)
  puts "#{response.code} #{response.message}"
  puts response.body
end