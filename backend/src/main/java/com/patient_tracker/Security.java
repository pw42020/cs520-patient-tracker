package com.patient_tracker;

import java.io.File;

import org.bouncycastle.util.io.pem.PemObject;
import org.bouncycastle.util.io.pem.PemReader;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.security.GeneralSecurityException;
import java.security.KeyFactory;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
// import RSA public and private keys
import java.security.interfaces.RSAPrivateKey;
import java.security.interfaces.RSAPublicKey;

import org.apache.logging.log4j.LogManager;
// add log4j
import org.apache.logging.log4j.Logger;

import java.security.PrivateKey;
import java.security.PublicKey;

public class Security {

    private static final Logger log = LogManager.getLogger("Security");

    /**
     * parse *.pem file
     * 
     * @param file
     * @return
     * @throws IOException
     */
    public static byte[] parsePEMFile(File file) throws IOException {
        if (!file.isFile() || !file.exists()) {
            throw new FileNotFoundException(String.format("The file '%s' doesn't exist.", file.getAbsolutePath()));
        }
        PemReader pemReader = new PemReader(new FileReader(file));
        PemObject pemObject = pemReader.readPemObject();
        // log.debug(pemObject.getContent());

        System.out.println("pemObject.getContent()");
        System.out.println(pemObject.getContent());
        return pemObject.getContent();
    }

    /**
     * read private key from file
     * 
     * @param file
     * @return
     * @throws IOException
     * @throws GeneralSecurityException
     */
    public static RSAPrivateKey readPKCS8PrivateKey(File file) throws IOException, GeneralSecurityException {
        byte[] content = parsePEMFile(file);
        PKCS8EncodedKeySpec keySpec = new PKCS8EncodedKeySpec(content);
        KeyFactory kf = KeyFactory.getInstance("RSA");
        return (RSAPrivateKey) kf.generatePrivate(keySpec);
    }

    /**
     * read public key from file
     * 
     * @param file
     * @return
     * @throws IOException
     * @throws GeneralSecurityException
     */
    public static RSAPublicKey readX509PublicKey(File file) throws IOException, GeneralSecurityException {
        byte[] content = parsePEMFile(file);

        X509EncodedKeySpec keySpec = new X509EncodedKeySpec(content);
        KeyFactory kf = KeyFactory.getInstance("RSA");
        return (RSAPublicKey) kf.generatePublic(keySpec);
    }
}
