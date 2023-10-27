package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"net/http"

	"./core"
)

func main() {
	demoAppApigw()
}

func demoAppApigw() {
	s := core.Signer{
		Key:    "apigateway_sdk_demo_key",
		Secret: "apigateway_sdk_demo_secret",
	}
	r, err := http.NewRequest("GET", "https://fake.dns.qihoo.net/apis/bifrost/ping?a=1&b=c",
		ioutil.NopCloser(bytes.NewBuffer([]byte("foo=bar"))))
	if err != nil {
		fmt.Println(err)
		return
	}

	r.Header.Add("content-type", "application/json; charset=utf-8")
	r.Header.Add("x-stage", "RELEASE")
	s.Sign(r)
	fmt.Println(r.Header)
	client := http.DefaultClient
	resp, err := client.Do(r)
	if err != nil {
		fmt.Println(err)
	}

	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println(err)
	}

	fmt.Println(string(body))
}
