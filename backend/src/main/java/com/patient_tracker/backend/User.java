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
    private String id;

    private DoctorPatient doctorPatient;
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

    // make getters and setters for every object
    public String getId() {
        return id;
    }
    public DoctorPatient getDoctorPatient() {
        return doctorPatient;
    }
    public String getName() {
        return name;
    }
    public String getDOB() {
        return DOB;
    }
    public String getPassword() {
        return password;
    }
    public String getSSN() {
        return SSN;
    }
    public List<String> getFormIds() {
        return formIds;
    }
    public String getGender() {
        return gender;
    }
    public String getAddress1() {
        return address1;
    }
    public String getAddress2() {
        return address2;
    }
    public String getCity() {
        return city;
    }
    public String getState() {
        return state;
    }
    public String getZip() {
        return zip;
    }
    public String getImageUrl() {
        return imageUrl;
    }
    public List<String> getAppointmentIds() {
        return appointmentIds;
    }
    public List<String> getAvailableSlots() {
        return availableSlots;
    }
    public void setId(String id) {
        this.id = id;
    }
    public void setDoctorPatient(DoctorPatient doctorPatient) {
        this.doctorPatient = doctorPatient;
    }
    public void setName(String name) {
        this.name = name;
    }
    public void setDOB(String DOB) {
        this.DOB = DOB;
    }
    public void setPassword(String password) {
        this.password = password;
    }
    public void setSSN(String SSN) {
        this.SSN = SSN;
    }
    public void setFormIds(List<String> formIds) {
        this.formIds = formIds;
    }
    public void setGender(String gender) {
        this.gender = gender;
    }
    public void setAddress1(String address1) {
        this.address1 = address1;
    }
    public void setAddress2(String address2) {
        this.address2 = address2;
    }
    public void setCity(String city) {
        this.city = city;
    }
    public void setState(String state) {
        this.state = state;
    }
    public void setZip(String zip) {
        this.zip = zip;
    }
    public void setImageUrl(String imageUrl) {
        this.imageUrl = imageUrl;
    }
    public void setAppointmentIds(List<String> appointmentIds) {
        this.appointmentIds = appointmentIds;
    }
    public void setAvailableSlots(List<String> availableSlots) {
        this.availableSlots = availableSlots;
    }

}
