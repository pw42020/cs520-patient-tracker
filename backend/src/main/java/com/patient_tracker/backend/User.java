package com.patient_tracker.backend;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
// import Gson
import com.google.gson.Gson;
// import jsonobject
import org.json.JSONObject;
// import lists
import java.util.List;

@Document("users")
public class User {

    enum DoctorPatient {
        DOCTOR,
        PATIENT
    }

    @Id
    public String id;

    public DoctorPatient doctorPatient;
    public String name;
    public String DOB;
    public String password;
    public String SSN;
    public List<String> formIds;
    public String gender;
    public String address1;
    public String address2;
    public String city;
    public String state;
    public String zip;
    public String imageUrl;
    public List<String> appointmentIds;
    public List<String> availableSlots;

    // public User(Gson userJson) {

    //     if ((int)userJson.get("doctorPatient") == 0) {
    //         this.doctorPatient = DoctorPatient.DOCTOR;
    //     } else {
    //         this.doctorPatient = DoctorPatient.PATIENT;
    //     }
    //     this.name = (String) userJson.get("name");
    //     this.DOB = (String) userJson.get("DOB");
    //     this.password = (String) userJson.get("password");
    //     this.SSN = (String) userJson.get("SSN");
    //     this.gender = (String) userJson.get("gender");
    //     this.address1 = (String) userJson.get("address1");
    //     this.address2 = (String) userJson.get("address2");
    //     this.city = (String) userJson.get("city");
    //     this.zip = (String) userJson.get("zip");
    //     this.imageUrl = (String) userJson.get("imageUrl");
    //     this.appointmentIds = (List<String>) userJson.get("appointmentIds");
    //     this.availableSlots = (List<String>) userJson.get("availableSlots");
    //     this.formIds = (List<String>) userJson.get("formIds");

    //     this.publicKey = (String) userJson.get("publicKey");
    //     this.privateKey = (String) userJson.get("privateKey");
    // }

    /**
     * convert user to json object
     * 
     * @return JSONObject
     */
    // public JsonObject toJson() {
    //     // add all parameters into a new json object
    //     JsonObject userJson = new JsonObject();
    //     userJson.put("doctorPatient", doctorPatient);
    //     userJson.put("name", name);
    //     userJson.put("DOB", DOB);
    //     userJson.put("password", password);
    //     userJson.put("SSN", SSN);
    //     userJson.put("gender", gender);

    //     userJson.put("address1", address1);
    //     userJson.put("address2", address2);
    //     userJson.put("city", city);
    //     userJson.put("zip", zip);
    //     userJson.put("imageUrl", imageUrl);
    //     userJson.put("appointmentIds", appointmentIds);
    //     userJson.put("availableSlots", availableSlots);
    //     userJson.put("formIds", formIds);

    //     userJson.put("publicKey", publicKey);
    //     userJson.put("privateKey", privateKey);

    //     return userJson;
    // }

}
