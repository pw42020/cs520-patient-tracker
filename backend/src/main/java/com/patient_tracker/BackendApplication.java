package com.patient_tracker.backend;
import org.json.JSONObject;

import com.patient_tracker.backend.User;
import com.patient_tracker.Security;

import java.io.File;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.io.IOException;
import java.security.GeneralSecurityException;

import java.io.FileInputStream;
import org.apache.commons.io.IOUtils;
import java.io.InputStream;

import java.io.FileNotFoundException;

import com.patient_tracker.backend.UserRepository;

// import Gson
import com.google.gson.Gson;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.boot.CommandLineRunner;


@EnableMongoRepositories
@RestController
@SpringBootApplication
public class BackendApplication implements CommandLineRunner{

	private static final Logger log = LogManager.getLogger("BackendApplication");
	private static final String MONGODB_KEY = System.getenv("MONGODB_KEY");

	@Autowired
	private UserRepository userRepository;

	@GetMapping("/")
	public String index() {
		return "Hello World!";
	}

	// @GetMapping("/users/{userId}")
	// public User getUser(@PathVariable String userId) {
	// return ;
	// }

	// add user to database
	// @PostMapping("/users")
	// public User createUser(@RequestParam String userJson) {
	// 	User user = new User(new JSONObject(userJson));
	// 	return user;
	// }
	
	public void createUsers() throws IOException, FileNotFoundException{
        File file = new File(System.getProperty("user.dir") + "/default_person.json");
		if (file.exists()) {
			InputStream is = new FileInputStream(System.getProperty("user.dir") + "/default_person.json");
            String jsonTxt = IOUtils.toString(is, "UTF-8");
            System.out.println(jsonTxt);
            Gson gson = new Gson();
			User user = gson.fromJson(jsonTxt, User.class);
			userRepository.save(user);
		}

    }

	@Override
    public void run(String...args) throws Exception {
        System.out.println(" ApplicationRunner called");
		try {
			createUsers();
		} catch (IOException e) {
			log.error(e.toString());
		}

		catch (Exception e) {
			log.error(e.toString());
		}
    }

	public static void main(String[] args) {

		try {
			PrivateKey privateKey = Security
					.readPKCS8PrivateKey(new File(System.getProperty("user.dir") + "/pkcs8.key"));
			PublicKey publicKey = Security
					.readX509PublicKey(new File(System.getProperty("user.dir") +
							"/publickey.crt"));

			// System.out.println(privateKey);
			// System.out.println(publicKey);
			// log.debug(publicKey);

			SpringApplication.run(BackendApplication.class, args);
		} catch (IOException e) {
			log.error(e.toString());
		} catch (GeneralSecurityException e) {
			log.error(e.toString());
		} catch (Exception e) {
			log.error(e.toString());
		}
	}

}
