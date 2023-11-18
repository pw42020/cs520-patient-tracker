// import junit
import org.junit.Test;

// import backendapplication.java
import com.patient_tracker.backend.BackendApplication;

class TestAPI {
    
    BackendApplication bA = null;
    String patientID = "anonymousPatient";
    String doctorID = "anonymousDoctor";

    @Before
    public void setUp() throws Exception {
        // create both doctor and patient
        bA = new BackendApplication();
        bA.createUserFromFile(System.getProperty("user.dir") + "/default_patient.json");
		bA.createUserFromFile(System.getProperty("user.dir") + "/default_patient.json");
    }

    @After
    public void tearDown() throws Exception {
        
        bA.deleteUserById(patientID);
        bA.deleteUserById(doctorID);
    }

    @Test
    public void getNewUser() {
        String checkPatientID = bA.getUser("anonymousPatient").getId();
        String checkDoctorID = bA.getUser("anonymousDoctor").getId();

        // assert both are the same as doctorID and patientID
        assertEqual(checkPatientID, patientID);
        assertEqual(checkDoctorID, doctorID);
    }
}