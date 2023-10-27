package com.test.appsignature;

import android.os.Handler;
import android.os.Message;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.*;

import com.cloud.apigateway.sdk.utils.Client;
import com.cloud.apigateway.sdk.utils.Request;
import okhttp3.Headers;
import okhttp3.OkHttpClient;
import okhttp3.Response;
import okhttp3.ResponseBody;
import org.json.JSONObject;

import java.util.Iterator;


public class MainActivity extends AppCompatActivity {
    private Handler handler = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        handler = new Handler() {
            @Override
            public void handleMessage(Message msg) {
                TextView result = findViewById(R.id.textViewResult);
                result.setText(msg.obj.toString());
            }
        };
        Button bt = findViewById(R.id.buttonSendRequest);
        bt.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        runTest();
                    }
                }).start();
            }
        });
    }

    private void runTest() {
        Request request = new Request();
        try {
            request.setKey(((EditText) findViewById(R.id.editTextAppKey)).getText().toString());
            request.setSecret(((EditText) findViewById(R.id.editTextAppSecret)).getText().toString());
            request.setMethod(((Spinner) findViewById(R.id.spinnerMethod)).getSelectedItem().toString());
            request.setUrl(((EditText) findViewById(R.id.editTextUrl)).getText().toString());
            try {
                JSONObject headers = new JSONObject(((EditText) findViewById(R.id.editTextHeaders)).getText().toString());
                Iterator<String> it = headers.keys();
                while (it.hasNext()) {
                    String key = it.next();
                    if (null != key && !"".equals(key)) {
                        request.addHeader(key, headers.getString(key));
                    }
                }
            } catch (Exception e) {
                Toast.makeText(MainActivity.this, "Fail parsing header json", Toast.LENGTH_LONG).show();
                return;
            }

            request.setBody(((EditText) findViewById(R.id.editTextBody)).getText().toString());
        } catch (Exception e) {
            e.printStackTrace();
            return;
        }
        try {
            //Sign the request.
            okhttp3.Request signedRequest = Client.signOkhttp(request);
            Headers headers = signedRequest.headers();
            StringBuffer sb = new StringBuffer();
            for (String h : headers.names()) {
                sb.append(h + ":" + headers.get(h) + "\n");
            }
            sb.append("------------\n");
            Message msg = Message.obtain();
            msg.obj = sb.toString();
            handler.sendMessage(msg);

            OkHttpClient.Builder httpClient = new OkHttpClient.Builder();
            OkHttpClient client = httpClient.build();
            Response response = client.newCall(signedRequest).execute();

            //Print the status line of the response.
            sb.append("status:" + response.code() + "\n");

            //Print the header fields of the response.
            Headers resHeaders = response.headers();
            for (String h : resHeaders.names()) {
                sb.append(h + ":" + resHeaders.get(h) + "\n");
            }

            //Print the body of the response.
            ResponseBody resEntity = response.body();
            if (resEntity != null) {
                sb.append("\n");
                sb.append(resEntity.string());
            }
            Message msg2 = Message.obtain();
            msg2.obj = sb.toString();
            handler.sendMessage(msg2);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }


}
