var sourceFile = document.getElementById("source");
var targetFile = document.getElementById("target");

function previewImage(event){
    const url = URL.createObjectURL(event.target.files[0]);
    const prevId = event.target.id + "Preview";
    document.getElementById(prevId).setAttribute("src", url);
}
sourceFile.addEventListener("change", previewImage);
targetFile.addEventListener("change", previewImage);


var rotatingSection = document.querySelector(".rotate-container");
var form = document.getElementById("form");
var swapBtn = document.getElementById("swap-btn");
var resultImage = document.getElementById("result-img");
var loader = document.getElementById("loader");

function showLoader(){
    loader.style.display = "flex";
}
function hideLoader(){
    loader.style.display = "none";
}

form.addEventListener("submit", async(e) => {
    e.preventDefault();

    if(!sourceFile.files[0]){
        alert("Please select source image!!!");
        return;
    }
    if(!targetFile.files[0]){
        alert("Please select target image!!!");
        return;
    }
    
    showLoader();

    const formData = new FormData();
    formData.append("source", sourceFile.files[0]);
    formData.append('target', targetFile.files[0])
    
    try{
        const response = await fetch("/swap", {
            method:"POST",
            body: formData
        })

        const output = await response.json();

        if(output.success === "true"){
            let path = resultImage.getAttribute("src");
            path = path.split("?")[0] + "?" + new Date();
            resultImage.setAttribute("src", path);
            rotatingSection.style.cssText = "transform: rotateY(180deg)";
        }else{
            alert("Unabel to swap face!!!");
        }
    }catch(err){
        console.log(err);
        alert("Error while swapping!");
    }
    hideLoader();
})

var backButton = document.getElementById("back");
backButton.addEventListener("click", () => {
    rotatingSection.style.cssText = "transform: rotateY(0deg)";
})


