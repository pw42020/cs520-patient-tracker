/**
 * @fileoverview Main file for encrypting and decrypting messages
 * from the MongoDB server.
 * @version 0.1.0
 */
// include JSEncrypt
const { JSEncrypt } = require('jsencrypt');

const MAX_BYTES = 117;

const { generateKeyPair, publicDecrypt, constants } = require('crypto');

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
        const dataToDecrypt = await response.json();
        let decryptedData = [];
        const decrypt = new JSEncrypt();
        decrypt.setPrivateKey(privateKey);
        for (let i = 0; i < dataToDecrypt["data"].length; i = i + MAX_BYTES) {
            console.log(i, i + MAX_BYTES);
            console.log(dataToDecrypt["data"].slice(i, i + MAX_BYTES));
            // update all into actual hex
            let turnToHex = dataToDecrypt["data"].slice(i, i + MAX_BYTES);
            let hexArray = [];
            for (let j = 0; j < dataToDecrypt["data"].slice(i, i + MAX_BYTES).length; j += 2) {
                hexArray[j / 2] = parseInt(turnToHex.substr(j, 2), 16);
            }
            console.log(hexArray);
            // decryptedData.push(publicDecrypt({
            //     key: privateKey,
            //     padding: require("crypto").constants.RSA_PKCS1_PSS_PADDING,
            //     oaepHash: "sha256",
            // }, Buffer.from(hexArray)));
            decryptedData.push(decrypt.decrypt(Buffer.from(hexArray)));
        }
        console.log(decryptedData);
        // return await response.json();
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
            format: 'pem'
        }
    }, async (err, publicKey, privateKey) => {
        // Handle errors and use the generated key pair.
        // console.log(publicKey);
        let response = await signIn("anonymousDoctor", "password", publicKey, privateKey);
        // console.log(response);
    });
}

main();