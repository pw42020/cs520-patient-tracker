package com.patient_tracker.backend;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

import com.patient_tracker.backend.Appointment;

public interface AppointmentRepository extends MongoRepository<Appointment, String> {

    @Query("{id:'?0'}")
    Appointment findAppointmentById(String id);

    // delete by id
    @Query("{id:'?0'}")
    void deleteAppointmentById(String id);
}