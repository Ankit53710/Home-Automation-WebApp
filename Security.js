import { storage, dbRef, listAll, getDownloadURL, uploadBytes, storageRef } from "./db.js";
// 📌 Fetch Live Images from "Live images/"
function fetchLiveImages() {
    const liveImagesContainer = document.getElementById("liveImagesContainer");
    liveImagesContainer.innerHTML = ""; // Clear previous content

    const liveImagesRef = storageRef(storage, "Live images/");

    listAll(liveImagesRef)
        .then((result) => {
            result.items.forEach((imageRef) => {
                getDownloadURL(imageRef).then((url) => {
                    const imgElement = document.createElement("img");
                    imgElement.src = url;
                    imgElement.classList.add("imgs");
                    imgElement.alt = "Live Image";
                    liveImagesContainer.appendChild(imgElement);
                });
            });
        })
        .catch((error) => console.log("Error fetching live images:", error));
}

function fetchAuthorizedUsers() {
    const authorizedUsersContainer = document.getElementById("authorizedUsersContainer");
    authorizedUsersContainer.innerHTML = ""; // Clear previous content

    const authorizedUsersRef = storageRef(storage, "Authorized_Users/");

    listAll(authorizedUsersRef)
        .then((result) => {
            let rowDiv = document.createElement("div");
            rowDiv.classList.add("row");

            result.items.forEach((imageRef, index) => {
                getDownloadURL(imageRef).then((url) => {
                    const userName = imageRef.name.split(".")[0]; // Extract name
                    const userDiv = document.createElement("div");
                    const imgElement = document.createElement("img");
                    const nameElement = document.createElement("div");

                    imgElement.src = url;
                    imgElement.classList.add("imgs");
                    imgElement.alt = userName;
                    nameElement.classList.add("Names");
                    nameElement.innerText = userName.replace(/_/g, " ");

                    userDiv.appendChild(imgElement);
                    userDiv.appendChild(nameElement);
                    userDiv.classList.add("user-card");

                    rowDiv.appendChild(userDiv);

                    // Every 5 users, create a new row
                    if ((index + 1) % 5 === 0 || index === result.items.length - 1) {
                        authorizedUsersContainer.appendChild(rowDiv);
                        rowDiv = document.createElement("div");
                        rowDiv.classList.add("row");
                    }
                });
            });
        })
        .catch((error) => console.log("Error fetching authorized users:", error));
}

// 📌 Upload Images to "Authorized_Users/"
function uploadImages() {
    const userName = document.getElementById("userName").value.trim();
    const fileInput = document.getElementById("fileInput");

    if (userName === "" || fileInput.files.length === 0) {
        alert("Please enter a name and upload at least one image.");
        return;
    }

    const uploadPromises = []; // To track uploads

    Array.from(fileInput.files).forEach((file, index) => {
        const fileRef = storageRef(storage, `Authorized_Users/${userName}/${userName}_${index + 1}.jpg`);
        uploadPromises.push(uploadBytes(fileRef, file));
    });

    // Wait for all uploads to complete
    Promise.all(uploadPromises)
        .then(() => {
            alert("Images uploaded successfully!");
            fetchAuthorizedUsers(); // Refresh the list after upload
        })
        .catch((error) => console.log("Upload error:", error));
}

// 📌 Fetch Images on Page Load
window.onload = function () {
    fetchLiveImages();
    fetchAuthorizedUsers();
};

document.getElementById("image-upload").addEventListener("click",uploadImages);