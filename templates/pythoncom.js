
// const slist = document.getElementById("Sounds")
//         const urlplay  = document.getElementById("UrlPlay")


function move(arg) {
    const dur = document.getElementById("Dur").value;
    if (dur.length == 0){dur = "1"}
    else if (dur <= 0){return }
    else if (dur > 9){return }
    $.getJSON("/move/"+arg+"/"+dur)
}


function ChangeLightanim(type,name)
{
    $.getJSON("/chng/"+type+"/"+name)
}
// Face
function loadfacebutton(loadobj,name)
{
    const h2 = document.createElement("button");
    const canv = document.createElement("img")

    canv.style = "position: relative;width: 64;left: 0;"
    canv.className="pixelated"
    canv.alt = name
    canv.src= "/Images/Eyes/"+name+".png"
    // h2.onclick = song.bind(null, name)
    h2.style = "width: 70; height: 70;align-items: center;margin:2px;background-color: black;"
    h2.title=name
    h2.onclick = ChangeLightanim.bind(null,"face", name)

    h2.append(canv)
    loadobj.appendChild(h2); 
}

//Head
function loadheadbutton(loadobj,name)
{
    const h2 = document.createElement("button");
    const canv = document.createElement("img")

    canv.style = "position: relative;width: 100%;"
    canv.className="pixelated"
    canv.alt = name
    canv.src= "/Images//Animations//"+name+".gif"
    h2.onclick = ChangeLightanim.bind(null,"head", name)
    h2.style = "width: 75; height: 75;align-items: center;margin:2px;background-color: black;"
    h2.title=name

    h2.append(canv)
    loadobj.appendChild(h2); 
}


// Sounds
function song(name)
{
    $.getJSON("/sound/play/"+name)
}
function playlink(input){
    link = input.value.replaceAll("/", "⠀").replaceAll("?","‎")
    // alert(link)
    song(link)
    input.value = ""
}
function playtext(input){
    link = input.value.replaceAll("/", "⠀").replaceAll("?","‎")
    // alert(link)
    song("text:"+link)
    input.value = "" 
}
function loadsoundbutton(loadobj,name)
{
    const h2 = document.createElement("button");
    text = name.replace("MafiaRobot_","")
    text = text.substring(0,text.indexOf("."))

    if (text.length > 13){
        text = text.substring(0, 13)
        text += "..."
    }

    h2.innerHTML = text
    h2.onclick = song.bind(null, name)
    h2.style = "width: 47.5%; height: 35;text-align: center;margin:2px"

    loadobj.appendChild(h2); 
}
function LoadSounds(loadobj)
{
    $.getJSON("/sound",function(data){
        data.forEach(async (name) => {
            loadsoundbutton(loadobj,name)
        });
    });
}


// Random
function generateRandomLetters(length) {
    const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890';
    let result = '';
    for (let i = 0; i < length; i++) {
      const randomIndex = Math.floor(Math.random() * alphabet.length);
      result += alphabet.charAt(randomIndex);
    }
    return result;
  }
function removeFromQueue(pos)
{
    console.log("removing "+pos+" from "+liwindow.location.hrefst)
}