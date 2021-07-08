function add() {
    document.getElementById("addtab").classList.add("active");
    document.getElementById("removetab").classList.remove("active");
    
    document.getElementById("add").style.display = "block";
    document.getElementById("remove").style.display = "none";
}

function remove() {
    document.getElementById("addtab").classList.remove("active");
    document.getElementById("removetab").classList.add("active");
    
    document.getElementById("add").style.display = "none";
    document.getElementById("remove").style.display = "block";
}