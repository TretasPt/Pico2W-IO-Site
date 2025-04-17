function a(){fetch('').then((r)=>console.log(r))}
console.log("js loaded");

function pressButton(target,value){
    fetch("", {
  method: "POST",
  body: JSON.stringify({
    //[target]: value,
    target: target,
    value: value,
  }),
  headers: {
    "Content-type": "application/json; charset=UTF-8"
  }
}).then(r=>{console.log(r)})
}