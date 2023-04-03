async function onSend() {
  let data = document.getElementById("messageInput");

  let message = data.value;

  const response = await fetch("http://example.com/movies.json", {
    method: "POST",

    body: JSON.stringify({ message })
  });

  const jsonData = await response.json();

  console.log(jsonData);
}

let eventSource = new EventSource("/listen");

eventSource.addEventListener(
  "message",
  function (e) {
    console.log(e, "message");

    let data = JSON.parse(e.data);

    const node = document.createElement("p");

    const textnode = document.createTextNode(data.message);

    node.appendChild(textnode);

    document.getElementById("messageWindow").appendChild(node);
    document.getElementById("messageWindow").scrollTop = document.getElementById("messageWindow").scrollHeight;
  },
  false
);

eventSource.addEventListener(
  "online",
  function (e) {
    console.log(e, "online");

    let data = JSON.parse(e.data);

    document.querySelector("#counter").innerText = data.counter;

    document.querySelector("body").style.backgroundColor = data.color;
  },
  true
);
