package com.patient_tracker.backend;
import org.json.JSONObject;

import com.patient_tracker.backend.User;
import com.patient_tracker.backend.Appointment;
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
import com.patient_tracker.backend.AppointmentRepository;

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
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

@EnableMongoRepositories
@RestController
@SpringBootApplication
public class BackendApplication implements CommandLineRunner{

	private static final Logger log = LogManager.getLogger("BackendApplication");
	private static final String MONGODB_KEY = System.getenv("MONGODB_KEY");

	@Autowired
	private UserRepository userRepository;

	@Autowired
	private AppointmentRepository appointmentRepository;

	public void createUserFromFile(String file_directory) throws FileNotFoundException, IOException{
		File file = new File(file_directory);
		if (file.exists()) {
			InputStream is = new FileInputStream(file_directory);
            String jsonTxt = IOUtils.toString(is, "UTF-8");
            System.out.println(jsonTxt);
            Gson gson = new Gson();
			User user = gson.fromJson(jsonTxt, User.class);
			log.info("user created with name " + user.getName());
			userRepository.save(user);
		} else {
			log.error("file not found");
		}
	}


	/**
	 * sign in with a username and password
	 * @param username user ID of the user
	 * @param password password of the user
	 * @return the user object if the password matches
	 */
	@GetMapping("/signin/{username}/{password}")
	public User signin(@PathVariable String username, @PathVariable String password) {
		User user = getUser(username);

		if (password.equals(user.getPassword())) {
			log.info("user signed in");
			return user;
		} else {
			log.error("incorrect password");
			throw new ResponseStatusException(HttpStatus.FORBIDDEN); 
		}
	}

	/**
	 * check if a user exists
	 * @param userId user ID of the user
	 * @return true if the user exists, false otherwise
	 */
	@GetMapping("/users/exists/{userId}")
	public boolean userExists(@PathVariable String userId) {
		if (userRepository.findUserById(userId) != null) {
			log.debug("user %s exists\n", userId);
			return true;
		} else {
			log.error("user %s does not exist\n", userId);
			return false;
		}
	}

	/**
	 * get a user by their ID
	 * @param userId user ID of the user
	 * @return the user object if the user exists, null otherwise
	 */
	@GetMapping("/users/{userId}")
	public User getUser(@PathVariable String userId) {
		User user = userRepository.findUserById(userId);
		if (user != null) {
			return user;
		} else {
			log.error("user not found");
			throw new ResponseStatusException(HttpStatus.NOT_FOUND); 
		}
	}

	/**
	 * delete a user by their ID
	 * @param userJson the full JSON of the user
	 * 
	 * Specificially requiring all JSON to prove that the user deleting
	 * this user is the user themself, we cannot have users deleting
	 * other users
	 */
	@GetMapping("/users/delete/{userJson}")
	public void deleteUser(@PathVariable String userJson) {
		Gson gson = new Gson();
		User user = gson.fromJson(userJson, User.class);
		String userId = user.getId();
		userRepository.deleteUserById(userId);
	}

	@PostMapping("appointments/create")
	public void createAppointment(@RequestParam String appointmentJson) {
		Gson gson = new Gson();
		Appointment appointment = gson.fromJson(appointmentJson, Appointment.class);
		appointmentRepository.save(appointment);

		// add appointment to user and doctor
		User user = userRepository.findUserById(appointment.getPatientId());
		user.addAppointment(appointment.getId());
		userRepository.save(user);

		User doctor = userRepository.findUserById(appointment.getDoctorId());
		doctor.addAppointment(appointment.getId());
		userRepository.save(doctor);
	}

	// create appointment


	/**
	 * create a new user (sign up)
	 * @param userJson json string of the user object, formatted in frontend
	 * @return the user object if the user is created successfully
	 */
	@PostMapping("/createUser")
	public User createUser(@RequestParam String userJson) {
		Gson gson = new Gson();
		User user = gson.fromJson(userJson, User.class);
		return userRepository.save(user);
	}

	/**
	 * run the initial setup for the backend if required
	 */
	@Override
    public void run(String...args) throws Exception {
        System.out.println(" ApplicationRunner called");
		// try {
		// 	createUsers();
		// } catch (IOException e) {
		// 	log.error(e.toString());
		// }

		// catch (Exception e) {
		// 	log.error(e.toString());
		// }
    }

	/**
	 * gets private and public keys for database and runs SpringBoot
	 */
	public static void main(String[] args) {

		try {
			PrivateKey privateKey = Security
					.readPKCS8PrivateKey(new File(System.getProperty("user.dir") + "/pkcs8.key"));
			PublicKey publicKey = Security
					.readX509PublicKey(new File(System.getProperty("user.dir") +
							"/publickey.crt"));

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
