package com.mdzz.together.network;

import android.content.Context;

import com.android.volley.RequestQueue;
import com.android.volley.toolbox.Volley;

import java.net.CookieHandler;
import java.net.CookieManager;

public class NetworkManager {
    private static NetworkManager instance = null;
    public RequestQueue queue;

    private NetworkManager() {
        NukeSSLCerts.nuke();
    }

    public static NetworkManager sharedManager(Context ctx) {
        if (instance == null) {
            instance = new NetworkManager();
            instance.queue = Volley.newRequestQueue(ctx.getApplicationContext());
            CookieHandler.setDefault(new CookieManager());
        }
        return instance;
    }

}