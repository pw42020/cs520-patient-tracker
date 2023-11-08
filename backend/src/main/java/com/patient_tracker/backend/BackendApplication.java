package com.patient_tracker.backend;

import org.json.JSONObject;

import com.patient_tracker.backend.User;
import com.patient_tracker.Security;

import java.io.File;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.io.IOException;
import java.security.GeneralSecurityException;

import org.apache.logging.log4j.LogManager;
// add log4j
import org.apache.logging.log4j.Logger;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestParam;

@RestController
@SpringBootApplication
public class BackendApplication {

	private static final Logger log = LogManager.getLogger("BackendApplication");

	@RequestMapping("/")
	public String home() {
		return "Hello World!";
	}

	// @GetMapping("/users/{userId}")
	// public User getUser(@PathVariable String userId) {
	// return ;
	// }

	// add user to database
	@PostMapping("/users")
	public User createUser(@RequestParam String userJson) {
		User user = new User(new JSONObject(userJson));
		return user;
	}

	public static void main(String[] args) {

		try {
			PrivateKey privateKey = Security
					.readPKCS8PrivateKey(new File(System.getProperty("user.dir") + "/pkcs8.key"));
			PublicKey publicKey = Security
					.readX509PublicKey(new File(System.getProperty("user.dir") +
							"/publickey.crt"));

			System.out.println(privateKey);
			System.out.println(publicKey);
			// log.debug(publicKey);

			// SpringApplication.run(BackendApplication.class, args);
		} catch (IOException e) {
			log.error(e.toString());
		} catch (GeneralSecurityException e) {
			log.error(e.toString());
		} catch (Exception e) {
			log.error(e.toString());
		}
	}

}
