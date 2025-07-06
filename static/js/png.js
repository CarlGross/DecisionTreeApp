document.addEventListener("DOMContentLoaded", () => {
    
    window.downloadPNG = function (filename) {
    const button = document.getElementById("pngButton");
    button.style.visibility = "hidden";
    html2canvas(document.documentElement).then(canvas => {
    const link = document.createElement('a');
    link.download = filename || "tree.png";
    link.href = canvas.toDataURL("image/png");
    link.click();
    button.style.visibility = "visible";
    });

}

});

