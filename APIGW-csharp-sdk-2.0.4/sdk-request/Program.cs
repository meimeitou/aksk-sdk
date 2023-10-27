using System;
using System.Net;
using System.IO;
using APIGATEWAY_SDK;
using System.Text;

namespace DEMO
{
    class Program
    {
        static void Main(string[] args)
        {
            ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12 | SecurityProtocolType.Tls11 | SecurityProtocolType.Tls;

            Signer signer = new Signer();
            //Set the AK/SK to sign and authenticate the request.
            signer.Key = "QTWAOYTTINDUT2QVKYUC";
            signer.Secret = "MFyfvK41ba2giqM7**********KGpownRZlmVmHc";

            //The following example shows how to set the request URL and parameters to query a VPC list.
            //Specify a request method, such as GET, PUT, POST, DELETE, HEAD, and PATCH.
            //Set request host.
            //Set request URI.
            //Set parameters for the request URL.
            HttpRequest r = new HttpRequest("GET",
                new Uri("https://fake.dns.qihoo.net/apis/bifrost/ping?a=1&b=c"));
            //Add a body if you have specified the PUT or POST method. Special characters, such as the double quotation mark ("), contained in the body must be escaped.
            r.body = "";

            //Add header parameters, for example, x-domain-id for invoking a global service and x-project-id for invoking a project-level service.
            r.headers.Add("Content-Type", "application/json");

            HttpWebRequest req = signer.Sign(r);
            Console.WriteLine(req.Headers.GetValues("x-sdk-date")[0]);
            Console.WriteLine(string.Join(", ", req.Headers.GetValues("authorization")));
            try
            {
                var writer = new StreamWriter(req.GetRequestStream());
                writer.Write(r.body);
                writer.Flush();
                HttpWebResponse resp = (HttpWebResponse)req.GetResponse();
                var reader = new StreamReader(resp.GetResponseStream());
                Console.WriteLine(reader.ReadToEnd());
            }
            catch (WebException e)
            {
                HttpWebResponse resp = (HttpWebResponse)e.Response;
                if (resp != null)
                {
                    Console.WriteLine((int)resp.StatusCode + " " + resp.StatusDescription);
                    var reader = new StreamReader(resp.GetResponseStream());
                    Console.WriteLine(reader.ReadToEnd());
                }
                else
                {
                    Console.WriteLine(e.Message);
                }

            }
        }

    }
}
