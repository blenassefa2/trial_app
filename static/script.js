const parallax=document.getElementById("div");

window.addEventListener("scroll",function(){
    let offset=window.pageYOffset;
    parallax.style.backgroundPositionY=offset*(0.68) +"px";
})
