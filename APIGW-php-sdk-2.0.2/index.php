<html>
<head>
    <title>PHP test</title>
</head>
<body>
<pre>
    <?php
    require 'signer.php';
    $signer = new Signer();
    //Set the AK/SK to sign and authenticate the request.
    $signer->Key = 'QTWAOYTTINDUT2QVKYUC';
    $signer->Secret = "MFyfvK41ba2giqM7**********KGpownRZlmVmHc";

    //The following example shows how to set the request URL and parameters to query a VPC list.
    //Specify a request method, such as GET, PUT, POST, DELETE, HEAD, and PATCH.
    //Set request Endpoint.
    //Set request URI.
    //Set parameters for the request URL.
    $req = new Request('GET', 'https://fake.dns.qihoo.net/apis/bifrost/ping?a=1&b=c');
    //Add header parameters, for example, x-domain-id for invoking a global service and x-project-id for invoking a project-level service.
    $req->headers = array(
        'content-type' => 'application/json',
    );
    //Add a body if you have specified the PUT or POST method. Special characters, such as the double quotation mark ("), contained in the body must be escaped.
    $req->body = '';
    $curl = $signer->Sign($req);

    var_dump($req->headers);
    echo "--------------\n";
    $response = curl_exec($curl);
    $status = curl_getinfo($curl, CURLINFO_HTTP_CODE);
    if ($status == 0) {
        echo curl_error($curl);
    } else {
        echo $status . "\n";
        echo $response;
    }
    curl_close($curl);
    ?>
</pre>
</body>
</html>