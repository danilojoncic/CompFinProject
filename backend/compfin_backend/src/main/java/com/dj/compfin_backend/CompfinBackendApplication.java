package com.dj.compfin_backend;

import jakarta.servlet.annotation.WebServlet;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.web.servlet.ServletRegistrationBean;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class CompfinBackendApplication {

    public static void main(String[] args) {
        SpringApplication.run(CompfinBackendApplication.class, args);
    }


}
