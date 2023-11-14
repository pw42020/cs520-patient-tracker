package com.patient_tracker.backend;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

@Document("appointments")
public class Appointment {
    
        @Id
        private String id;
    
        private String doctorId;
        private String patientId;
        private String dateTime;
        private String reason;
    
        public String getId() {
            return id;
        }
        public String getDoctorId() {
            return doctorId;
        }
        public String getPatientId() {
            return patientId;
        }
        public String getDateTime() {
            return dateTime;
        }
        public String getReason() {
            return reason;
        }
        public void setId(String id) {
            this.id = id;
        }
        public void setDoctorId(String doctorId) {
            this.doctorId = doctorId;
        }
        public void setPatientId(String patientId) {
            this.patientId = patientId;
        }
        public void setDateTime(String dateTime) {
            this.dateTime = dateTime;
        }
        public void setReason(String reason) {
            this.reason = reason;
        }
}