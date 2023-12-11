/**
 * @fileoverview Main file for encrypting and decrypting messages
 * from the MongoDB server.
 * @version 0.1.0
 */

const { generateKeyPair } = require('crypto');

async function signIn(username, password, publicKey, privateKey) {
    const response = await fetch(`http://127.0.0.1:5000/sign_in`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "username": username, "password": password, "publicKey": publicKey })
    });

    if (response.ok) {
        // if the response is 200, return the json after unencrypting it
        console.log("Hello world");
        // const dataToDecrypt = await response.json();
        // for (let i = 0; i < dataToDecrypt.length; i++) {
        //     console.log(dataToDecrypt[i]);
        //     dataToDecrypt[i] = decrypt(dataToDecrypt[i], privateKey);
        // }
        // return await response.json();
        return "hi";
    } else if (response.status === 404) {
        return null;
    }
}

/**
 * Main function for the program.
 * @return {void}
 */
async function main() {
    console.log("Hello World!");
    // generates a public and private key pair
    // for use in the database.
    generateKeyPair('rsa', {
        modulusLength: 1024,
        publicKeyEncoding: {
            type: 'pkcs1',
            format: 'pem'
        },
        privateKeyEncoding: {
            type: 'pkcs1',
            format: 'pem',
        }
    }, async (err, publicKey, privateKey) => {
        // Handle errors and use the generated key pair.
        console.log(publicKey);
        let response = await signIn("anonymousDoctor", "password", publicKey);
        // console.log(response);
    });
}

main();