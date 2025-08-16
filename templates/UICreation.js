var SideOpen = ""
const Sidebar = document.getElementById("Sidebar")
var bottompos = 0
const istemp = window.location.href.search("templates") != -1


// Side bar opening
function SideBarButton(Section,url="")
{
  
  if (window.location.href.endsWith(url)){
    if (istemp)
    {
      url = "index.html"
    }else{
      url = "/"
    }
  }
  else{ if (istemp){ url += ".html" } }
  window.location.assign(url)
} 

// Side bar button adding
function SideButton(Name,Icon,html)
{
  button = document.createElement("button")
  img = document.createElement("img")

  button.style = 'width: 50; height: 50;right: -50;float: right; position: absolute;bottom: '+bottompos+"; border-radius: 5px;"
  button.title=Name
  button.onclick = SideBarButton.bind(null,Name,html)
  button.id = "SideButton"


  img.style = "width: 45;height: 45;position: absolute;top: 2;left: 3;"
  img.src = Icon

  button.append(img)
  Sidebar.append(button)
  bottompos += button.offsetHeight+5
}
 
function BoolValue(Val)
{
  console.log(Val)
}

function Queue(parent, name, val,pos)
{
  div = document.createElement("div")
  p = document.createElement("p")
  button = document.createElement("button")
  img = document.createElement("img")

  div.style = "width: 100%;height: 35;position: relative;"
  p.style = "left: 0;position: absolute; top: -25;"

  if (pos > -1)
  {
    button.style = "position: absolute;right: 0;top: 5;"
    img.src = "/Images/Trash.png"
    img.alt="Delete"
    div.append(button)
    button.append(img)
    button.onclick = removeFromQueue.bind(null,p)
  }

  if (/^-?\d+(\.\d+)?$/.test(val))
  {
    val = Math.ceil(val * 100) / 100
  }
  if (name.length > 12){
    name = name.substring(0, 12)
    name += "..."
  }
  p.innerHTML = name +" | "+val

    div.append(p)
  parent.append(div)
}

// preperations
SideButton("Movement","../Images/Movement.png","Movement")
SideButton("Sound","../Images/Sounds.png","Sounds")
SideButton("Eyes","../Images/Eyes.png","Eyes")
SideButton("Head","../Images/Top.png","Lights")
