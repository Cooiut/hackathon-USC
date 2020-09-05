package com.mdzz.together;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.os.Bundle;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.google.android.material.textfield.TextInputEditText;

import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

import com.mdzz.together.network.NetworkManager;
import com.mdzz.together.network.Server;

public class LoginActivity extends AppCompatActivity {

    private TextInputEditText username;
    private TextInputEditText password;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        setTitle("登录"); // TODO: 9/4/2020
        username = findViewById(R.id.username);
        password = findViewById(R.id.password);

    }

    @Override
    public void onRestart() {
        super.onRestart();
        password.setText("");
    }

    private void login() {
        String email = Objects.requireNonNull(username.getText()).toString();
        String pwd = Objects.requireNonNull(password.getText()).toString();

        if (email.isEmpty()) {
            username.setError(getString(R.string.username_not_entered));
            return;
        }

        if (pwd.isEmpty()) {
            password.setError(getString(R.string.password_not_entered));
            return;
        }

        RequestQueue queue = NetworkManager.sharedManager(this).queue;
        StringRequest loginRequest = new StringRequest(Request.Method.POST,
                Server.server + "login", LoginActivity.this::success, this::error) {
            @Override
            protected Map<String, String> getParams() {
                Map<String, String> params = new HashMap<>();
                params.put("email", email);
                params.put("password", pwd);
                return params;
            }
        };
        queue.add(loginRequest);
    }

    private void success(String response) {
        // TODO: 9/4/2020  用户名密码检查
        Toast.makeText(LoginActivity.this, "登录成功", Toast.LENGTH_SHORT).show();
        startActivity(new Intent(LoginActivity.this, MainActivity.class));
        // TODO: 9/4/2020  用户存入session
    }

    @SuppressLint("SetTextI18n")
    private void error(VolleyError error) {
        // Log.d("login", "Error: " + error.toString());
        Toast.makeText(LoginActivity.this, "用户名或密码错误！", Toast.LENGTH_SHORT).show();
    }
}