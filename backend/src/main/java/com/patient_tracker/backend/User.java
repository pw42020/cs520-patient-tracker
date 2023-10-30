package com.patient_tracker.backend;

import org.springframework.data.mongodb.core.mapping.Document;
// import jackson
import org.json.JSONObject;

// import lists
import java.util.List;

@Document("users")
public class User {

    enum DoctorPatient {
        DOCTOR,
        PATIENT
    }

    public DoctorPatient doctorPatient;
    private String name;
    private String DOB;
    private String password;
    private String SSN;
    private List<String> formIds;
    private String gender;
    private String address1;
    private String address2;
    private String city;
    private String state;
    private String zip;
    private String imageUrl;
    private List<String> appointmentIds;
    private List<String> availableSlots;

    private String publicKey;
    private String privateKey;

    public User(JSONObject userJson) {
        this.doctorPatient = (DoctorPatient) userJson.get("doctorPatient");
        this.name = (String) userJson.get("name");
        this.DOB = (String) userJson.get("DOB");
        this.password = (String) userJson.get("password");
        this.SSN = (String) userJson.get("SSN");
        this.gender = (String) userJson.get("gender");
        this.address1 = (String) userJson.get("address1");
        this.address2 = (String) userJson.get("address2");
        this.city = (String) userJson.get("city");
        this.zip = (String) userJson.get("zip");
        this.imageUrl = (String) userJson.get("imageUrl");
        this.appointmentIds = (List<String>) userJson.get("appointmentIds");
        this.availableSlots = (List<String>) userJson.get("availableSlots");
        this.formIds = (List<String>) userJson.get("formIds");

        this.publicKey = (String) userJson.get("publicKey");
        this.privateKey = (String) userJson.get("privateKey");
    }

    /**
     * convert user to json object
     * 
     * @return JSONObject
     */
    public JSONObject toJson() {
        // add all parameters into a new json object
        JSONObject userJson = new JSONObject();
        userJson.put("doctorPatient", doctorPatient);
        userJson.put("name", name);
        userJson.put("DOB", DOB);
        userJson.put("password", password);
        userJson.put("SSN", SSN);
        userJson.put("gender", gender);

        userJson.put("address1", address1);
        userJson.put("address2", address2);
        userJson.put("city", city);
        userJson.put("zip", zip);
        userJson.put("imageUrl", imageUrl);
        userJson.put("appointmentIds", appointmentIds);
        userJson.put("availableSlots", availableSlots);
        userJson.put("formIds", formIds);

        userJson.put("publicKey", publicKey);
        userJson.put("privateKey", privateKey);

        return userJson;
    }

}
