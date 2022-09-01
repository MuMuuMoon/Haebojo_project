package com.ex.myqr;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.TypedValue;
import android.view.Gravity;
import android.view.View;
import android.widget.ImageButton;
import me.toptas.fancyshowcase.FancyShowCaseView;


public class MainActivity extends AppCompatActivity {


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        new FancyShowCaseView.Builder(this)
                .title("HAEBOJO")
                .titleStyle(R.style.Font, Gravity.CENTER)
                .titleSize(60, TypedValue.COMPLEX_UNIT_SP)
                .build()
                .show();

        ImageButton scanQRBtn = findViewById(R.id.QR);

        scanQRBtn.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, ScanQR.class);
                startActivity(intent);
            }
        });
    }
}
