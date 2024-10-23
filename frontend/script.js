async function doSomething() {
    const inputText = document.getElementById("inputText1").value;
    const response = await fetch('/paraphrase',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({text:inputText})
    });
    const outputText = document.getElementById("inputText2");
    if(response.ok){
        const data = await response.json();
        outputText.value = data.paraphrasedText;
    }else{
        outputText.value = "Something went wrong";
    }
}

document.getElementById("inputText1").addEventListener('input',()=>{
    document.getElementById("wordcount").innerText = document.getElementById("inputText1").value.split(" ").length;
});

document.getElementById("btnaction").addEventListener('click',doSomething);