

document.addEventListener('DOMContentLoaded', function () {
    let textToType = "Welcome to Flash Fleet."
    // </br>Enter Your Details";
    // const typingSpeed = 40;
    const typingSpeed = 1;
    
    const typingElement = document.getElementById("typing-effect");
    let charIndex = 0;
    
    const form = document.getElementById("main_form");
    const continueBtn = document.createElement("button");
    continueBtn.innerHTML = "Continue";
    continueBtn.id="continueButtonLogin";
    const br = document.createElement("br");
    const brEle = document.createElement("br");
    const div = document.getElementById("form-group");
    const span_id=document.createElement("span");
    
    var enter=false;
    let factor=0;
    function typeText() {
        if (charIndex < textToType.length - 1) {
            let str = typingElement.innerHTML;
            if (str.length-factor == 0) {
                typingElement.innerHTML += textToType.charAt(charIndex) + "|";
            }
            else {
                typingElement.innerHTML = typingElement.innerHTML.slice(0, -1) + textToType.charAt(charIndex) + "|";
            }
    
            charIndex++;
            setTimeout(typeText, typingSpeed);
        }
        else if (charIndex == textToType.length-1) {
            typingElement.innerHTML = typingElement.innerHTML.slice(0, -1) + textToType.charAt(charIndex);
    
            charIndex++;
            setTimeout(typeText, typingSpeed);
        }
        else if((charIndex>=textToType.length) && (enter==false)){
            enter=true;
            typingElement.innerHTML+="<br><br>";
            textToType="Enter Your Details. ";
            charIndex=0;
            factor=typingElement.textContent.length+8;
    
            setTimeout(typeText, typingSpeed);
        }
        else {
            const label1 = document.createElement("label");
            label1.for = "name";
            label1.innerHTML = "Enter your name";
            const namein = document.createElement("input");
            
            span_id.innerHTML='Already have an account?Click <i class="here">here</i>';
            span_id.id="create"
            
            const brr=document.createElement("br");
        
            namein.type = "text";
            namein.placeholder = "Name";
            namein.name = "name";
            namein.classList.add("inpp"); 
            namein.required;
            form.appendChild(label1);
            form.appendChild(br);
            form.appendChild(namein);
            form.appendChild(brEle);
            div.appendChild(continueBtn);
            div.appendChild(brr);
            div.appendChild(span_id);
        }
    
    }
    
    window.onload = typeText;
    
    var num = 1;
    var correct = true;
    var match = true;
    continueBtn.addEventListener("click", function () {
        if (num == 1) {
            var nam = document.myform.name.value;
            for (let i = 0; i < nam.length; i++) {
                if (!isNaN(nam.charAt(i)) && nam.charAt(i) != " ") {
                    correct = false;
                }
            }
    
            if (nam.length == 0) {
                match = false;
            }
        }
    
        else if (num == 2) {
            // let unum = document.myform.uname.value;

                //Username validation
        }
    
        if (correct && match) {
            const label1 = document.createElement("label");
            let br1 = document.createElement("br");
            let br2 = document.createElement("br");
            label1.for = "name";
            label1.innerHTML = "Enter your name";
    
    
            const label2 = document.createElement("label");
            label2.for = "uname";
            label2.innerHTML = "Enter your Username";
            const phonein = document.createElement("input");
            phonein.type = "text";
            phonein.placeholder = "Username";
            phonein.classList.add("inpp");
            phonein.name = "uname";
    
            const label3 = document.createElement("label");
            label3.for = "pswd";
            label3.innerHTML = "Enter your password";
            const mailin = document.createElement("input");
            mailin.name="pswd";
            mailin.type = "password";
            mailin.classList.add("inpp");
            mailin.placeholder = "Password";
    
            const sub = document.createElement("input");
            sub.type = "submit";
            sub.value = "Enter";
            sub.id="submit";
            if (num == 1) {
                form.appendChild(label2);
                form.appendChild(br1);
                form.appendChild(phonein);
                form.appendChild(br2);
    
                num++;
            }
            else if (num == 2) {
                form.appendChild(label3);
                form.appendChild(br1);
                form.appendChild(mailin);
                form.appendChild(br2);
                form.appendChild(sub);
                div.removeChild(continueBtn);
                num++;
            }
            // form.insertBefore(newFormGroup, continueBtn);
        }
        else {
            if (num == 1) {
                if (correct == false) {
                    window.alert("Name cannot have number");
                    correct = true;
                }
                if (match == false) {
                    window.alert("Name cannot be blank");
                    match = true;
                }
            }
    
            else if (num == 2) {
                if (correct == false) {
                    window.alert("Phone Number can only have numbers");
                    correct = true;
                    match = true;
                }
                else if (match == false) {
                    window.alert("Phone Number should have 10 digits");
                    correct = true;
                    match = true;
                }
    
            }
        }
    });
    
    
    const div2=document.getElementById("register-form");
    const span_id2=document.getElementById("create2");
    span_id.addEventListener('click',function(){
        div.style.display="none";
        div2.style.display="block";
    });

    span_id2.addEventListener('click',function(){
        div.style.display="block";
        div2.style.display="none";
    })

});
