package com.patient_tracker.backend;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

import com.patient_tracker.backend.User;

public interface UserRepository extends MongoRepository<User, String> {

    @Query("{name:'?0'}")
    User findUserByName(String name);

    @Query("{id:'?0'}")
    User findUserById(String id);

    // delete by id
    @Query("{id:'?0'}")
    void deleteUserById(String id);
}
